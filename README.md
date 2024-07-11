---
layout: default
---
<main>
  <section>
    <div style="text-align: center;">
      <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
      <a class="search-link" href="https://ib.bsb.br/tags">TAGS</a>
    </div>
    {% assign date_format = site.sleek.date_format | default: "%b %-d, %Y" %}
    {% assign sorted_posts = site.posts | sort: 'last_modified_at' | reverse %}
    {% for post in sorted_posts %}
      <article>
        <span >
        <!-- <time>{{ post.last_modified_at_str }}</time> -->
        <time>{{ post.last_modified_at | date: date_format }}</time>
        <!-- <time>{{ post.date | date: date_format }}</time> -->
        <a style="color:#33ccff;" href="{{ post.url }}">
            <img src="https://raw.githubusercontent.com/marioseixas/marioseixas.github.io/main/assets/gold.ico" alt="favicon">
            {{ post.title }}
          </a>
        </span>
      </article>
    {% endfor %}
  </section>
</main>
