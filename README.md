<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>infoBAG</title>
  <style>
    /* Existing styles */
    time {
      color: #16A085;
    }
    a {
      color: #D35400;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }

    /* Refactored styles from GitHub code */
    body {
      font-family: BitPotionExt;
      max-width: 100%;
      margin: 0 auto;
      padding: 20px;
    }
    main {
      text-align: center;
      color: #FFFFFF;
    }
    section {
      text-align: center;
      color: #666;
    }
    article {
      list-style: none;
      padding: 0;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
    }
    article time {
      margin: 5px;
    }
    a {
      color: #0066cc;
      text-decoration: none;
      transition: color 0.3s ease;
    }
    a:hover {
      color: #004080;
    }
    section {
      margin-top: 40px;
    }
    h1 {
      border-bottom: 2px solid #0066cc;
      padding-bottom: 5px;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin-bottom: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 15px;
    }
    li:last-child {
      border-bottom: none;
    }
    a {
      color: #FFFFFF;
      text-decoration: none;
      transition: color 0.3s ease;
      font-size: 1.2em;
      display: block;
      margin-bottom: 5px;
    }
    a:hover {
      color: #0066cc;
    }
    time {
      font-size: 0.9em;
      color: #888;
      display: block;
    }
    .back-link {
      margin-top: 40px;
      text-align: center;
    }
    @media (max-width: 600px) {
      body {
        padding: 10px;
      }
      main {
        font-size: 1.5em;
      }
      a {
        font-size: 1em;
      }
    }
  </style>
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
