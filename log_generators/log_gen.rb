# log_gen.rb — Auto-push logger (Ruby)
# Usage:
#   require_relative '../log_generators/log_gen'
#   LogGen.start
#   LogGen.log("kuch bhi")
#   LogGen.stop

require 'digest'
require 'fileutils'
require 'time'

module LogGen
  WS       = ENV['GITHUB_WORKSPACE'] || '.'
  OUT      = "#{WS}/output"
  RUNTIME  = "#{OUT}/runtimelogs.txt"
  DETAILED = "#{OUT}/detailedlog.txt"

  @last_hash = nil
  @thread    = nil

  def self._ts = Time.now.utc.strftime('%Y-%m-%d %H:%M:%S UTC')

  def self._hash
    c = [RUNTIME, DETAILED].map { |f| File.read(f) rescue '' }.join
    Digest::MD5.hexdigest(c)
  end

  def self._git(*args) = system('git', *args, chdir: WS, out: '/dev/null', err: '/dev/null')

  def self._push
    h = _hash
    return if h == @last_hash          # kuch badla nahi — skip!
    @last_hash = h
    _git('add', 'output/')
    return if system('git diff --staged --quiet', chdir: WS, out: '/dev/null')
    _git('commit', '-m', "🔄 #{Time.now.utc.strftime('%H:%M:%S')}")
    _git('pull', '--rebase', 'origin', 'main')
    _git('push')
  end

  def self.log(msg, level = 'INFO')
    FileUtils.mkdir_p(OUT)
    line = "[#{_ts}] [#{level}] #{msg}"
    puts line
    File.open(RUNTIME, 'a') { |f| f.puts line }
  end

  def self.start
    FileUtils.mkdir_p(OUT)
    log('🚀 LogGen started!')
    @thread = Thread.new { loop { sleep 5; _push } }
  end

  def self.stop
    @thread&.kill
    log('🏁 LogGen stopped — final push...')
    _push
  end
end
