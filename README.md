<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      {% assign posts_with_sort_date = site.posts | map: "last_modified_at" %}
      {% for post in site.posts %}
        {% assign post_date = post.date | date: "%Y-%m-%d" %}
        {% assign last_modified_date = post.last_modified_at | date: "%Y-%m-%d" %}
        {% if last_modified_date and last_modified_date != post_date %}
          {% assign sort_date = post.last_modified_at %}
        {% else %}
          {% assign sort_date = post.date %}
        {% endif %}
        {% assign post = post | merge: { 'sort_date': sort_date } %}
        {% assign posts_with_sort_date = posts_with_sort_date | push: post %}
      {% endfor %}
      {% assign sorted_posts = posts_with_sort_date | sort: 'sort_date' | reverse %}
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
