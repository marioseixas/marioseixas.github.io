<style>
  .quote1 { font-size: 1.5em; color: #ff0000; }
  .quote2 { font-style: italic; color: #00ff00; }
  .quote3 { background-color: #ffff00; color: #0000ff; }
</style>
<main>
  <section>
    <p class="quote1">say to yourself what you would be; do what you gotta do; do well</p>
    <p class="quote2">progress is wrecked or preserved by a single event</p>
    <p class="quote3">can't steer unless already moving</p>
  </section>
  <section>
    {% for post in site.posts %}
    <article>
      <time datetime="{{ post.date | date: "%Y-%m-%d" }}">
        {{ post.date | date: "%Y-%m-%d" }}
      </time>
      <a href="{{ post.url }}">
        {{ post.title }}
      </a>
    </article>
    {% endfor %}
  </section>
  <footer>
    <p>
      <a title='GitHub' target="_blank" rel="noreferrer" href="https://github.com/marioseixas/marioseixas.github.io">
        GitHub
      </a>
    </p>
  </footer>
</main>
