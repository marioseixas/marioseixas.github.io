<html lang="en">
<body>
  <main class="tags-page">
    <section>
      <!-- Sort posts by last_modified_at, falling back to date -->
      {% assign sorted_posts = site.posts | sort: 'last_modified_at', 'date', nils: 'last' | reverse %}

      <!-- Loop through all sorted posts and display them -->
      {% for post in sorted_posts %}
        <article class="post-item">
          <time datetime="{{ post.date | date: '%Y-%m-%d' }}" class="post-date">
            {{ post.date | date: '%Y-%m-%d' }}
             ~>  
            {% if post.last_modified_at %}
              {{ post.last_modified_at | date_to_string }}
            {% else %}
              {{ post.date | date_to_string }}
            {% endif %}            
            <a class="post-link" href="{{ post.url }}">
              <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
              {{ post.title }}
            </a>
          </time>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
