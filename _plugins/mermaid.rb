# frozen_string_literal: true

module Jekyll
  class RenderMermaid < Liquid::Block
    def render(context)
      # Capture the content inside the block and strip unnecessary whitespace
      text = super.strip

      # Wrap the content inside a <div> with appropriate classes and styles
      mermaid_script = generate_mermaid_script
      mermaid_div = "<div class='mermaid' style='white-space: pre-wrap;'>#{text}</div>"

      # Return the script and div as a single string without any additional processing
      "#{mermaid_script}#{mermaid_div}"
    end

    private

    def generate_mermaid_script
      <<~SCRIPT
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        <script type='module'>
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
          mermaid.initialize({
            startOnLoad: true,
            theme: 'dark',
            er: { useMaxWidth: true }
          });
          setTimeout(() => {
            svgPanZoom(document.querySelector("div.mermaid>svg"), {
              minZoom: 0.5,
              maxZoom: 10,
              fit: true,
              contain: false,
              controlIconsEnabled: true,
              center: true,
              refreshRate: "auto",
            });
          }, 200);
        </script>
      SCRIPT
    end
  end
end

# Register the custom tag with Liquid
Liquid::Template.register_tag('mermaid', Jekyll::RenderMermaid)
