---
layout: null
permalink: /index.html
id: index
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
  <div class="wrapper">
    <main class="iframe-container">
      <iframe name="embed_readwrite" src="https://pad.ouvaton.coop/short-ref?alwaysShowChat=true&showLineNumbers=true&useMonospaceFont=true&noColors=true" frameborder="0" title="Embedded Pad"></iframe>
    </main>
  </div>
</body>
