---
layout: default
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ site.title | default: "infoBAG" }}</title>
</head>
<body>
  <main>
    <section>
      {% assign sorted_posts = site.posts | sort: 'last_modified_at', 'date' | reverse %}
      {% for post in sorted_posts %}
        <article>
          {% assign display_date = post.last_modified_at | default: post.date %}
          <time datetime="{{ display_date | date_to_xmlschema }}" style="color: #16A085;">
            {{ display_date | date: "%Y-%m-%d" }}
          </time>
          <a style="color:#D35400;" href="{{ post.url | relative_url }}">
            <img src="{{ '/assets/gold.ico' | relative_url }}" alt="Article icon" width="16" height="16">
            {{ post.title }}
            &nbsp;&middot;
            {% if post.last_modified_at %}
              Last modified: {{ post.last_modified_at | date: "%b %-d, %Y" }}
            {% else %}
              Created: {{ post.date | date: "%b %-d, %Y" }}
            {% endif %}
          </a>
        </article>
      {% endfor %}
    </section>
  </main>
</body>
</html>
