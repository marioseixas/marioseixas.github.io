#!/usr/bin/env ruby
require 'yaml'
require 'find'
# Loop through all markdown files in the _posts directory
Find.find('./_posts') do |path|
  next unless File.file?(path) && File.extname(path) == '.md'
  # Get the last modified date from Git
  last_modified = `git log -1 --format=%cd --date=iso -- #{path}`.strip
  
  # If Git date is not available, use file's mtime
  if last_modified.empty?
    last_modified = File.mtime(path).iso8601
  end
  # Read the current content of the file
  content = File.read(path)
  # Parse the front matter
  if content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
    front_matter = YAML.load($1)
    content_body = $'
  else
    front_matter = {}
    content_body = content
  end
  # Update the last_modified_at in the front matter
  front_matter['last_modified_at'] = last_modified
  # Write the updated content back to the file
  File.write(path, "---\n#{front_matter.to_yaml}---\n#{content_body}")
end
