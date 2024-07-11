require 'open3'
module Jekyll
  module Revision
    class Generator < Jekyll::Generator
      def generate(site)
        return if site.data['git_log'] == false
        return if ARGV.include?("--no-revision")
        %w(posts).each do |type|
          site.send(type).docs.each do |item|
            item.data['last_modified_at'] = GitLogger.new(site.source, item.path).last_modified_at
          end
        end
        puts("FINISH: post-data-revision")
      end
    end
    class GitLogger
      attr_reader :site_source, :page_path
      def initialize(site_source, page_path)
        @site_source = site_source
        @page_path   = page_path
      end
      def last_modified_at
        return nil unless is_git_repo?
        log = Executor.sh('git', 'log', '-1', '--format=%ct', relative_path_from_git_dir)
        log.to_i
      end
      private
      def is_git_repo?
        @@is_git_repo ||= begin
          Dir.chdir(site_source) do
            Executor.sh("git", "rev-parse", "--is-inside-work-tree").eql? "true"
          end
        rescue
          false
        end
      end
      def absolute_path_to_article
        @article_file_path ||= Jekyll.sanitized_path(site_source, @page_path)
      end
      def relative_path_from_git_dir
        @relative_path_from_git_dir ||= Pathname.new(absolute_path_to_article)
          .relative_path_from(
            Pathname.new(File.dirname(top_level_git_directory))
          ).to_s
      end
      def top_level_git_directory
        @@top_level_git_directory ||= begin
          Dir.chdir(site_source) do
            File.join(Executor.sh("git", "rev-parse", "--show-toplevel"), ".git")
          end
        rescue
          ""
        end
      end
    end
    module Executor
      def self.sh(*args)
        Open3.popen2e(*args) do |stdin, stdout_stderr, wait_thr|
          exit_status = wait_thr.value # wait for it...
          output = stdout_stderr.read
          output ? output.strip : nil
        end
      end
    end
  end
end
