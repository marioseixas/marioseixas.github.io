<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign posts_with_sort_keys = site.posts %}
      {% for post in site.posts %}
        {% if post.last_modified_at != post.date %}
          {% assign sort_key = post.last_modified_at %}
        {% else %}
          {% assign sort_key = post.date %}
        {% endif %}
        {% assign post_with_key = post | merge: {'sort_key': sort_key | date: '%Y%m%d%H%M%S'} %}
        {% assign posts_with_sort_keys = posts_with_sort_keys | push: post_with_key %}
      {% endfor %}
      {% assign sorted_posts = posts_with_sort_keys | sort: 'sort_key' | reverse %}
      {% for post in sorted_posts %}
        <article>
          <time datetime="{{ post.date | date: '%Y-%m-%d' }}" style="color: #16A085;">
            {{ post.date | date: '%Y-%m-%d' }}
            <a style="color:#D35400;" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }} &nbsp;&middot; {{ post.last_modified_at | date_to_string }}
            </a>
          </time>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
