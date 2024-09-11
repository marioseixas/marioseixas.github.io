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
      post = context.registers[:post]
      app_id = "5fce21a3-9b85-4794-b6f6-e0eaaf788ced"
      post_id = post['id']
      post_url = "#{site.config['url']}#{post['url']}"
      post_title = post['title']

      uri = URI.parse("https://cusdis.com/api/open/comments?appId=#{app_id}&pageId=#{post_id}")
      response = Net::HTTP.get_response(uri)

      if response.is_a?(Net::HTTPSuccess)
        data = JSON.parse(response.body)
        Jekyll.logger.info "CusdisComments:", "Fetched comments data: #{data.inspect}"
        render_comments(data, app_id, post_id, post_url, post_title)
      else
        Jekyll.logger.error "CusdisComments:", "Failed to load comments: #{response.message}"
        "<!-- Failed to load comments: #{response.message} -->"
      end
    rescue => e
      Jekyll.logger.error "CusdisComments:", "Error: #{e.message}"
      "<!-- Error loading comments: #{e.message} -->"
    end

    private

    def render_comments(data, app_id, post_id, post_url, post_title)
      comments = extract_comments(data)
      <<-HTML
        <div id="cusdis_thread"
          data-host="https://cusdis.com"
          data-app-id="#{app_id}"
          data-post-id="#{post_id}"
          data-post-url="#{post_url}"
          data-post-title="#{post_title}"
        >
          <h3>Comments (#{comments.length})</h3>
          #{render_comment_list(comments)}
        </div>
        <script async defer src="https://cusdis.com/js/cusdis.es.js"></script>
      HTML
    end

    def extract_comments(data)
      if data['data'] && data['data']['data'].is_a?(Array)
        data['data']['data']
      else
        Jekyll.logger.warn "CusdisComments:", "No valid comments array found in data: #{data.inspect}"
        []
      end
    end

    def render_comment_list(comments)
      comments.map do |comment|
        if comment.is_a?(Hash)
          render_single_comment(comment)
        else
          Jekyll.logger.warn "CusdisComments:", "Invalid comment data: #{comment.class}"
          "<p>Invalid comment data</p>"
        end
      end.join
    end

    def render_single_comment(comment)
      <<-HTML
        <div class="comment">
          <p><strong>#{comment['by_nickname'] || 'Anonymous'}</strong></p>
          <p>#{comment['content'] || 'No content'}</p>
          #{comment['post_title'] ? "<p>post: #{comment['post_title']}</p>" : ''}
          #{comment['project_title'] ? "<p>Project: #{comment['project_title']}</p>" : ''}
        </div>
      HTML
    end
  end
end

Liquid::Template.register_tag('cusdis_comments', Jekyll::CusdisCommentsTag)
