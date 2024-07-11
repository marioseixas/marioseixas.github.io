#!/usr/bin/env ruby
require 'yaml'
require 'find'
require 'time'
def ensure_time(value)
  return Time.parse(value).strftime('%Y-%m-%d %H:%M:%S %z') if value.is_a?(String)
  return value.strftime('%Y-%m-%d %H:%M:%S %z') if value.is_a?(Time)
  Time.now.strftime('%Y-%m-%d %H:%M:%S %z')
end
Find.find('.') do |path|
  next unless File.file?(path) && ['.md', '.html'].include?(File.extname(path))
  content = File.read(path)
  if content =~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
    front_matter = YAML.safe_load($1)
    content_body = $'
  else
    next
  end
  git_date = `git log -1 --format=%cd --date=iso -- #{path}`.strip
  last_modified = git_date.empty? ? File.mtime(path) : Time.parse(git_date)
  
  front_matter['last_modified_at'] = ensure_time(last_modified)
  File.write(path, "---\n#{front_matter.to_yaml}---\n#{content_body}")
end
