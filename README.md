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
        <a href="https://ib.bsb.br/life-tokens">can't steer unless already moving</a>
      </div>
      <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
      <a class="search-link" href="https://ib.bsb.br/tags">TAGS</a>
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}" style="color: #efef00;"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a style="color:#33ccff;" href="{{ post.url }}">
                <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon" style="margin-left: 5px; vertical-align: middle;">
                {{ post.title }}
            </a>
        </article> 
        {% endfor %}
    </section>
</main>
</body>
</html>
