module Jekyll
  module TagFilter
    def contains_tag(tags, tag)
      tags = tags.first if tags.is_a?(Array) && tags.first.is_a?(Array) # Handle nested arrays
      tags = tags.map(&:strip) if tags.is_a?(Array)
      tags.any? { |t| t == tag || t.start_with?(tag + ">") }
    end
  end
end

Liquid::Template.register_filter(Jekyll::TagFilter)
