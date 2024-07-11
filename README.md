<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      <div style="text-align: center;">
        <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
        <a class="search-link" href="https://ib.bsb.br/tags">TAGS</a>
      </div>
      {% assign sorted_posts = site.posts | sort: 'last_modified_at' | reverse %}
      {% for post in sorted_posts %}
        <article>
          <time datetime="{{ post.date | date: '%Y-%m-%d' }}" style="color: #efef00;">{{ post.date | date: '%Y-%m-%d' }}</time>
          <a style="color:#33ccff;" href="{{ post.url }}">
            <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
            {{ post.title }}
          </a>
          {% assign modified_date = post.last_modified_at | date: '%Y-%m-%d' %}
          {% assign created_date = post.date | date: '%Y-%m-%d' %}
          {% if modified_date != created_date %}
            <time datetime="{{ post.last_modified_at | date: '%Y-%m-%d' }}" style="color: #ffffff;">
              ed @{{ modified_date }}
            </time>
          {% endif %}
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
