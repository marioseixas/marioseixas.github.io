<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign posts_with_modified = site.posts | where: 'last_modified_at' %}
      {% assign posts_without_modified = site.posts | where_exp: "post", "post.last_modified_at == nil" %}
      
      {% assign sorted_with_modified = posts_with_modified | sort: 'last_modified_at' | reverse %}
      {% assign sorted_without_modified = posts_without_modified | sort: 'date' | reverse %}
      
      {% assign sorted_posts = sorted_with_modified | concat: sorted_without_modified %}
      
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
