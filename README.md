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
      {% for post in site.posts %} 
        <article>
          <time datetime="{{ post.date | date: "%Y-%m-%d" }}" style="color: #efef00;"> {{ post.date | date: "%Y-%m-%d" }} </time>
          <a style="color:#33ccff;" href="{{ post.url }}">
            <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
            {{ post.title }}
          </a>
          {% assign created_date = post.date | date: "%Y-%m-%d" %}
          {% assign modified_date = post.last_modified_at | date: "%Y-%m-%d" %}
          {% if post.last_modified_at and created_date != modified_date %}
            modified <time datetime="{{ post.last_modified_at | date_to_xmlschema }}">
              {{ post.last_modified_at | date: date_format }}
            </time>
          {% endif %}
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
