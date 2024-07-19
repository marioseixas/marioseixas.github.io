<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
</head>
<body>
  <main>
    <section>
      <!-- Separate posts with and without last_modified_at -->
      {% assign posts_with_last_modified = site.posts | where_exp: "post", "post.last_modified_at" %}
      {% assign posts_without_last_modified = site.posts | where_exp: "post", "post.last_modified_at == nil" %}
      
      <!-- Sort posts with last_modified_at by last_modified_at in descending order -->
      {% assign sorted_posts_with_last_modified = posts_with_last_modified | sort: 'last_modified_at' | reverse %}
      
      <!-- Sort posts without last_modified_at by date in descending order -->
      {% assign sorted_posts_without_last_modified = posts_without_last_modified | sort: 'date' | reverse %}
      
      <!-- Concatenate the two sorted lists -->
      {% assign all_sorted_posts = sorted_posts_with_last_modified | concat: sorted_posts_without_last_modified %}
      
      <!-- Loop through all sorted posts and display them -->
      {% for post in all_sorted_posts %}
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
