<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign posts_with_sort_keys = site.posts | map: 'last_modified_at' %}
      {% assign posts_with_sort_keys = "" %}
      {% for post in site.posts %}
        {% assign last_modified = post.last_modified_at | default: post.date %}
        {% assign sort_key = last_modified | date: '%Y%m%d%H%M%S' %}
        {% assign post_with_key = post | push: sort_key %}
        {% capture posts_with_sort_keys %}{{ posts_with_sort_keys }}{{ post_with_key }}{% endcapture %}
      {% endfor %}
      {% assign sorted_posts = posts_with_sort_keys | split: '' | sort: '1' | reverse %}
      {% for post in sorted_posts %}
        <article>
          <time datetime="{{ post.date | date: '%Y-%m-%d' }}" style="color: #16A085;">
            {{ post.date | date: '%Y-%m-%d' }}
            <a style="color:#D35400;" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }} &nbsp;&middot; {{ post.last_modified_at | default: post.date | date_to_string }}
            </a>
          </time>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
