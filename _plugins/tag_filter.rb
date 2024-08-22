module Jekyll
  module TagFilter
    def contains_tag(tags, tag)
      tags = tags.first if tags.is_a?(Array) && tags.first.is_a?(Array)
      tags = tags.join(',').split(',').map(&:strip) if tags.is_a?(Array)
      tag_parts = tag.split('>')
      tags.any? do |t|
        t == tag || tag_parts.all? { |part| t.include?(part) }
      end
    end
  end
end

Liquid::Template.register_filter(Jekyll::TagFilter)
