// LogGen.java — Auto-push logger (Java)
// Usage:
//   import log_generators.LogGen;
//   LogGen.start();
//   LogGen.log("kuch bhi");
//   LogGen.stop();

package log_generators;

import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.*;

public class LogGen {
    private static final String WS       = System.getenv("GITHUB_WORKSPACE") != null
                                            ? System.getenv("GITHUB_WORKSPACE") : ".";
    private static final String OUT      = WS + "/output";
    private static final String RUNTIME  = OUT + "/runtimelogs.txt";
    private static final String DETAILED = OUT + "/detailedlog.txt";
    private static final DateTimeFormatter FMT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss 'UTC'");

    private static String lastHash = null;
    private static ScheduledExecutorService scheduler;

    private static String ts() {
        return ZonedDateTime.now(ZoneOffset.UTC).format(FMT);
    }

    private static String hash() {
        try {
            String c = "";
            for (String f : new String[]{RUNTIME, DETAILED})
                try { c += Files.readString(Path.of(f)); } catch (Exception ignored) {}
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] b = md.digest(c.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte x : b) sb.append(String.format("%02x", x));
            return sb.toString();
        } catch (Exception e) { return ""; }
    }

    private static void git(String... args) {
        try {
            String[] cmd = new String[args.length + 3];
            cmd[0] = "git"; cmd[1] = "-C"; cmd[2] = WS;
            System.arraycopy(args, 0, cmd, 3, args.length);
            new ProcessBuilder(cmd).redirectErrorStream(true)
                .start().waitFor();
        } catch (Exception ignored) {}
    }

    private static synchronized void push() {
        String h = hash();
        if (h.equals(lastHash)) return;         // kuch badla nahi — skip!
        lastHash = h;
        git("add", "output/");
        try {
            int rc = new ProcessBuilder("git","-C",WS,"diff","--staged","--quiet")
                .start().waitFor();
            if (rc == 0) return;
        } catch (Exception ignored) {}
        git("commit", "-m", "🔄 " + ZonedDateTime.now(ZoneOffset.UTC).format(
            DateTimeFormatter.ofPattern("HH:mm:ss")));
        git("pull", "--rebase", "origin", "main");
        git("push");
    }

    public static void log(String msg) { log(msg, "INFO"); }
    public static void log(String msg, String level) {
        try {
            Files.createDirectories(Path.of(OUT));
            String line = "[" + ts() + "] [" + level + "] " + msg;
            System.out.println(line);
            Files.writeString(Path.of(RUNTIME), line + "\n",
                StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        } catch (Exception ignored) {}
    }

    public static void start() {
        try { Files.createDirectories(Path.of(OUT)); } catch (Exception ignored) {}
        log("🚀 LogGen started!");
        scheduler = Executors.newSingleThreadScheduledExecutor();
        scheduler.scheduleAtFixedRate(LogGen::push, 5, 5, TimeUnit.SECONDS);
    }

    public static void stop() {
        if (scheduler != null) scheduler.shutdown();
        log("🏁 LogGen stopped — final push...");
        push();
    }
}
