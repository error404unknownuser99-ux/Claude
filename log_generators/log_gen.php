<?php
/**
 * log_gen.php — Auto-push logger (PHP)
 * Usage:
 *   require_once __DIR__ . '/../log_generators/log_gen.php';
 *   LogGen::start();
 *   LogGen::log("kuch bhi");
 *   LogGen::stop();
 */

class LogGen {
    private static string $ws;
    private static string $out;
    private static string $runtime;
    private static string $detailed;
    private static ?string $lastHash = null;
    private static ?int $pid = null;

    public static function init(): void {
        self::$ws       = getenv('GITHUB_WORKSPACE') ?: '.';
        self::$out      = self::$ws . '/output';
        self::$runtime  = self::$out . '/runtimelogs.txt';
        self::$detailed = self::$out . '/detailedlog.txt';
    }

    private static function ts(): string {
        return gmdate('Y-m-d H:i:s') . ' UTC';
    }

    private static function hash(): string {
        $c = '';
        foreach ([self::$runtime, self::$detailed] as $f)
            if (file_exists($f)) $c .= file_get_contents($f);
        return md5($c);
    }

    private static function git(string ...$args): void {
        $cmd = 'git -C ' . escapeshellarg(self::$ws) . ' '
             . implode(' ', array_map('escapeshellarg', $args))
             . ' > /dev/null 2>&1';
        exec($cmd);
    }

    private static function push(): void {
        $h = self::hash();
        if ($h === self::$lastHash) return;     // kuch badla nahi — skip!
        self::$lastHash = $h;
        self::git('add', 'output/');
        exec('git -C ' . escapeshellarg(self::$ws) . ' diff --staged --quiet', result_code: $rc);
        if ($rc === 0) return;
        self::git('commit', '-m', '🔄 ' . gmdate('H:i:s'));
        self::git('pull', '--rebase', 'origin', 'main');
        self::git('push');
    }

    public static function log(string $msg, string $level = 'INFO'): void {
        if (!is_dir(self::$out)) mkdir(self::$out, 0755, true);
        $line = '[' . self::ts() . '] [' . $level . '] ' . $msg;
        echo $line . PHP_EOL;
        file_put_contents(self::$runtime, $line . PHP_EOL, FILE_APPEND);
    }

    public static function start(): void {
        self::init();
        if (!is_dir(self::$out)) mkdir(self::$out, 0755, true);
        self::log('🚀 LogGen started!');
        // Background push via shell loop
        $script = 'while true; do sleep 5; php -r \'
            require "' . __FILE__ . '";
            LogGen::init();
        \'; done';
        self::$pid = (int) exec("bash -c " . escapeshellarg($script) . " > /dev/null 2>&1 & echo $!");
        file_put_contents('/tmp/log_gen_pid', self::$pid);
    }

    public static function stop(): void {
        $pid = (int) @file_get_contents('/tmp/log_gen_pid');
        if ($pid) exec("kill $pid 2>/dev/null");
        self::log('🏁 LogGen stopped — final push...');
        self::push();
    }
}

// Auto-init
LogGen::init();
