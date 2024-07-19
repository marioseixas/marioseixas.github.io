<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      <!-- Separate posts where last_modified_at is different from date -->
      {% assign modified_posts = site.posts | where_exp: "post", "post.last_modified_at != post.date" %}
      {% assign unmodified_posts = site.posts | where_exp: "post", "post.last_modified_at == post.date" %}
      
      <!-- Sort modified posts by last_modified_at in descending order -->
      {% assign sorted_modified_posts = modified_posts | sort: 'last_modified_at' | reverse %}
      
      <!-- Sort unmodified posts by date in descending order -->
      {% assign sorted_unmodified_posts = unmodified_posts | sort: 'date' | reverse %}
      
      <!-- Concatenate the two sorted lists -->
      {% assign all_sorted_posts = sorted_modified_posts | concat: sorted_unmodified_posts %}
      
      <!-- Loop through all sorted posts and display them -->
      {% for post in all_sorted_posts %}
        <article>
          <time datetime="{{ post.date | date: "%Y-%m-%d" }}" style="color: #16A085;">
            {{ post.date | date: "%Y-%m-%d" }}
            <a style="color:#D35400;" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }} &nbsp;&middot; 
              {% if post.last_modified_at != post.date %}
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
