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
        <a href="https://ib.bsb.br/categories/">can't steer</a>
        <a href="https://ib.bsb.br/404.html">unless</a>
        <a href="https://ib.bsb.br/tags/">already moving</a>
      </div>
      <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a style="color:#33ccff;" href="{{ post.url }}"> {{ post.title }} </a> <!-- Changes post title color for readability -->
        </article> 
        {% endfor %}
    </section>
</main>
</body>
</html>
