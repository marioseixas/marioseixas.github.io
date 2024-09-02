module Jekyll
  class CodeBlockTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @language = text.strip # Extract the language from the tag (e.g., "python")
    end

    def render(context)
      # Extract the code block content while handling potential indentation
      code_content = super.strip.gsub(/^\s+/, "")

      # Build data-src attribute based on language 
      filename = "code-block.#{@language}"

      # Build data-download-link-label attribute
      download_label = "Download #{@language.capitalize()} Code"

      # Construct the HTML output
      "<section data-src=\"#{filename}\" data-download-link data-download-link-label=\"#{download_label}\" class=\"language-#{@language}\"><code class=\"language-#{@language}\">#{code_content}</code></section>"
    end
  end
end

Liquid::Template.register_tag('codeblock', Jekyll::CodeBlockTag)
