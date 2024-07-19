<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign posts_with_sort_keys = "" %}
      {% for post in site.posts %}
        {% assign sort_date = post.last_modified_at | default: post.date %}
        {% assign post_with_key = post | merge: {'sort_key': sort_date | date: '%s'} %}
        {% capture posts_with_sort_keys %}{{ posts_with_sort_keys }}{% unless forloop.first %},{% endunless %}{{ post_with_key }}{% endcapture %}
      {% endfor %}
      {% assign posts_array = posts_with_sort_keys | split: ',' %}
      {% assign sorted_posts = posts_array | sort: 'sort_key' | reverse %}
      {% for post in sorted_posts %}
        {% assign post = site.posts | where: "url", post.url | first %}
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
