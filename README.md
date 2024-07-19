<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
  <style>
    .tags-page {
      font-family: BitPotionExt;
      max-width: device-width;
      margin: 0 auto;
      padding: 20px;
    }
    .post-item {
      margin-bottom: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 15px;
    }
    .post-item:last-child {
      border-bottom: none;
    }
    .post-link {
      color: #FFFFFF;
      text-decoration: none;
      transition: color 0.3s ease;
      font-size: 1.2em;
      display: block;
      margin-bottom: 5px;
    }
    .post-link:hover {
      color: #0066cc;
    }
    .post-date {
      font-size: 0.9em;
      color: #888;
      display: block;
    }
    @media (max-width: 600px) {
      .tags-page {
        padding: 10px;
      }
      .post-link {
        font-size: 1em;
      }
    }
  </style>
</head>
<body>
  <main class="tags-page">
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
        <article class="post-item">
          <time datetime="{{ post.date | date: '%Y-%m-%d' }}" class="post-date" style="color: #16A085;">
            {{ post.date | date: '%Y-%m-%d' }}
            <a class="post-link" href="{{ post.url }}">
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
