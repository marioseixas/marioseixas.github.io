module Jekyll
  class CodeBlockTag < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      @language = markup.strip
    end

    def render(context)
      code_content = super.strip.gsub(/^\s+/, "") # Remove leading whitespace
      filename = "code-block.#{@language}"         # Create a meaningful filename 
      download_label = "Download #{@language.capitalize()} Code"

      # Encode code content for use in a data URI
      encoded_content = URI.encode_www_form_component(code_content) 
      data_uri = "data:text/plain;charset=utf-8,#{encoded_content}"

      # Construct the HTML output with the data URI in data-src
      "<section data-src=\"#{data_uri}\" data-download-link data-download-link-label=\"#{download_label}\" class=\"language-#{@language}\"><code class=\"language-#{@language}\">#{code_content}</code></section>"
    end
  end
end

Liquid::Template.register_tag('codeblock', Jekyll::CodeBlockTag)
