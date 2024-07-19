<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign sorted_posts = site.posts | sort: 'last_modified_at', 'first' | reverse %}
      {% for post in sorted_posts %}
        <article>
          <time datetime="{{ post.date | date: "%Y-%m-%d" }}" style="color: #16A085;">
            {{ post.date | date: "%Y-%m-%d" }}
            <a style="color:#D35400;" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }} &nbsp;&middot; 
              {% if post.last_modified_at %}
                {{ post.last_modified_at | date_to_string }}
              {% else %}
                {{ post.date | date_to_string }}
              {% endif %}
            </a>
          </time>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
