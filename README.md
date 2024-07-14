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
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}" style="color: #16A085;">
              {{ post.date | date: "%Y-%m-%d" }}
              <a style="color:#D35400;" href="{{ post.url }}">
                <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
                {{ post.title }} &nbsp;&middot; {{ page.last_modified_at | date_to_string }}
                {% assign modified_date = page.last_modified_at | date: "%Y-%m-%d" %}
              </a>
            </time>
        </article>
    {% endfor %}
  </section>
</main>
</body>
</html>
