# frozen_string_literal: true

module Jekyll
    class RenderMermaid < Liquid::Block
      def render(context)
        text = super
        mermaid_script = generate_mermaid_script
        mermaid_pre = "<pre class='mermaid'> #{text}  </pre>"
  
        "#{mermaid_script}#{mermaid_pre}"
      end
  
      private
  
      def generate_mermaid_script
        <<~SCRIPT
          <script type='module'>
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
    startOnLoad: true,
    theme: 'dark',
    er: { useMaxWidth: true }
  });
  setTimeout(() => {
    svgPanZoom(document.querySelector("#mermaid-pre>svg"), {
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
  
  Liquid::Template.register_tag('mermaid', Jekyll::RenderMermaid)
