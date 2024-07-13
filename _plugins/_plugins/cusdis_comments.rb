require 'net/http'
require 'uri'
require 'json'

module Jekyll
  class CusdisCommentsTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @text = text
    end

    def render(context)
      site = context.registers[:site]
      page = context.registers[:page]

      app_id = "5fce21a3-9b85-4794-b6f6-e0eaaf788ced"
      page_id = page['id']
      page_url = "#{site.config['url']}#{site.config['baseurl']}#{page['url']}"
      page_title = page['title']

      uri = URI.parse("https://cusdis.com/api/open/comments?appId=#{app_id}&pageId=#{page_id}")
      response = Net::HTTP.get_response(uri)

      if response.is_a?(Net::HTTPSuccess)
        comments = JSON.parse(response.body)['data']
        render_comments(comments, app_id, page_id, page_url, page_title)
      else
        "<!-- Failed to load comments: #{response.message} -->"
      end
    end

    private

    def render_comments(comments, app_id, page_id, page_url, page_title)
      html = <<-HTML
        <div id="cusdis_thread"
          data-host="https://cusdis.com"
          data-app-id="#{app_id}"
          data-page-id="#{page_id}"
          data-page-url="#{page_url}"
          data-page-title="#{page_title}"
        >
          <h3>Comments</h3>
          #{render_comment_list(comments)}
        </div>
        <script async defer src="https://cusdis.com/js/cusdis.es.js"></script>
      HTML

      html
    end

    def render_comment_list(comments, depth = 0)
      html = ""
      comments.each do |comment|
        html += <<-HTML
          <div class="comment" style="margin-left: #{depth * 20}px;">
            <p><strong>#{comment['by']}</strong> - #{comment['created_at']}</p>
            <p>#{comment['content']}</p>
            #{render_comment_list(comment['replies'], depth + 1)}
          </div>
        HTML
      end
      html
    end
  end
end

Liquid::Template.register_tag('cusdis_comments', Jekyll::CusdisCommentsTag)
