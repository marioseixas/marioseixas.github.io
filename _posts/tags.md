---
layout: null
title: Tags
permalink: /tags.html
id: tags
---

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>
    {% if page.id == "home" %}
      {{ site.title }}
    {% else %}
      {{ page.title }} — {{ site.title }}
    {% endif %}
  </title>

  <link rel="canonical" href="{{ page.canonical_url | default: site.url | append: page.url }}">
  <link rel="alternate" type="application/rss+xml" title="{{ site.title }}" href="{{ site.baseurl }}/rss.xml">

  <meta property="og:site_name" content="{{ site.title }}">
  <meta property="og:title" content="{{ page.title | default: site.title }}">
  <meta property="og:type" content="{% if page.title %}article{% else %}website{% endif %}">
  <meta property="og:url" content="{{ site.url }}{{ page.url }}">
  
  {% if page.image %}
    <meta property="og:image" content="{{ page.image | prepend: site.url }}">
  {% endif %}

  {% if page.date %}
    <meta property="article:published_time" content="{{ page.date | date_to_xmlschema }}">
    <meta property="article:author" content="{{ page.author | default: site.author }}">
  {% endif %}

  {% if page.tags %}
    <meta itemprop="keywords" content="{{ page.tags | join: ',' }}">
    {% for tag in page.tags %}
      <meta property="article:tag" content="{{ tag }}">
    {% endfor %}
  {% endif %}

  <link href="{{ '/style.css' | relative_url }}" rel="stylesheet">
  <link href="{{ '/pagefind/pagefind-ui.css' | relative_url }}" rel="stylesheet">
  <script src="{{ '/pagefind/pagefind-ui.js' | relative_url }}"></script>
  <script type="module">
    import PagefindHighlight from '{{ "/pagefind/pagefind-highlight.js" | relative_url }}';
    new PagefindHighlight({ highlightParam: "highlight" });
  </script>
  <script src="{{ '/assets/js/search.js' | relative_url }}" defer></script>    
</head>
<body>
  <a class="search-input-block" id="search"></a>
  <header>
    <nav aria-label="Main navigation">
      <div class="header-container">
        <a class="internal-link" href="/">
          <img src="{{ '/assets/Sudden_Death_Rune.gif' | relative_url }}" alt="Sudden Death Rune" class="favicon">
        </a>
        <a href="https://ib.bsb.br/archive">
          <img src="{{ '/favicon.ico' | relative_url }}" alt="Archive Icon" class="favicon">
        </a>
        <a href="https://ib.bsb.br/tags">
          <img src="{{ '/assets/Label.gif' | relative_url }}" alt="Tags Icon" class="favicon">
        </a>
        <a href="https://ib.bsb.br/events">
          <img src="{{ '/assets/Paralyse_Rune.gif' | relative_url }}" alt="Events Icon" class="favicon">
        </a>
      </div>
    </nav>
  </header>
  <div class="post-wrapper">    
    <div class="tag-page">
      <h1>{{ page.title }}</h1>
      <ul class="tag-list" aria-label="List of all tags">
  {% for tag_data in site.data.processed_tags %}
    {% assign has_highlighted_post = false %}
    {% for post in tag_data.posts %}
      {% if post.highlighted %}
        {% assign has_highlighted_post = true %}
        {% break %}
      {% endif %}
    {% endfor %}

    {% if has_highlighted_post %}
      <li>
        <a href="#{{ tag_data.tag | slugify }}" aria-label="Tag {{ tag_data.tag }} with {{ tag_data.posts.size }} posts">
          {{ tag_data.tag }} ({{ tag_data.posts.size }})
        </a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
    </div>
    <main class="tagged-posts">
  {% for tag_data in site.data.processed_tags %}
    <section class="search-link" id="{{ tag_data.tag | slugify }}" aria-labelledby="{{ tag_data.tag | slugify }}-heading">
      <h2 id="{{ tag_data.tag | slugify }}-heading">
        <a href="#" class="back-to-top" aria-label="Back to top">
          <img src="{{ '/assets/gold.ico' | relative_url }}" alt="gold icon">
        </a>
        {{ tag_data.tag }}
      </h2>
      <ul>
        {% for post in tag_data.posts %}
        <li>
            <a href="{{ post.url }}">
              {% if post.highlighted %}
                <mark>{{ post.title }}</mark>
              {% else %}
                {{ post.title }}
              {% endif %}
            </a>
          </li>
        {% endfor %}
      </ul>
    </section>
  {% endfor %}
    </main>
  </div>
</body>