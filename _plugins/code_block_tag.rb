module Jekyll
  class CodeBlockTag < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      @language = markup.strip
    end

    def render(context)
      code_content = super.strip.gsub(/^\s+/, "")
      filename = "code-block.#{@language}"
      download_label = "Download #{@language.capitalize()} Code"

      # Determine MIME type 
      mime_type = case @language
                  when "python" then "text/x-python"
                  when "html" then "text/html"
                  when "javascript" then "text/javascript"
                  when "css" then "text/css"
                  when "ruby" then "text/x-ruby"
                  when "bash", "shell" then "text/x-sh"
                  when "json" then "application/json"
                  when "xml" then "application/xml"
                  when "yaml" then "text/yaml"
                  when "markdown" then "text/markdown"
                  when "java" then "text/x-java"
                  when "c" then "text/x-c"
                  when "cpp" then "text/x-c++"
                  when "csharp" then "text/x-csharp"
                  when "go" then "text/x-go"
                  when "php" then "text/x-php"
                  when "swift" then "text/x-swift"
                  when "typescript" then "text/typescript"
                  when "sql" then "text/x-sql"
                  when "dockerfile" then "text/x-dockerfile"
                  when "makefile" then "text/x-makefile"
                  else "text/plain" # Default 
                  end

      # Encode code content for data URI
      encoded_content = URI.encode_www_form_component(code_content)
      data_uri = "data:#{mime_type};charset=utf-8,#{encoded_content}"

      # Construct HTML output
      "<section data-src=\"#{data_uri}\" data-download-link data-download-link-label=\"#{download_label}\" data-download=\"#{filename}\" class=\"language-#{@language}\"><code class=\"language-#{@language}\">#{code_content}</code></section>"
    end
  end
end

Liquid::Template.register_tag('codeblock', Jekyll::CodeBlockTag)
