<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign sorted_posts = site.posts | sort: 'last_modified_at' | reverse %}
      {% for post in sorted_posts %}
        <article>
          {% assign display_date = post.last_modified_at | default: post.date %}
          <time datetime="{{ display_date | date: "%Y-%m-%d" }}" style="color: #16A085;">
            {{ display_date | date: "%Y-%m-%d" }}
            <a style="color:#D35400;" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }} &nbsp;&middot; {{ display_date | date_to_string }}
            </a>
          </time>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
