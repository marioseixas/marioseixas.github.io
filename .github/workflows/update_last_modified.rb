#!/usr/bin/env ruby
require 'yaml'
require 'find'
Find.find('./_posts') do |path|
  next unless File.file?(path) && File.extname(path) == '.md'
  content = File.read(path)
  if content =~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
    front_matter = YAML.safe_load($1)
    content_body = $'
  else
    next
  end
  # Use Unix timestamp (seconds since epoch)
  front_matter['last_modified_at'] = File.mtime(path).to_i
  File.write(path, "---\n#{front_matter.to_yaml}---\n#{content_body}")
end
