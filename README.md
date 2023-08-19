<main>
  <section>
    <p>say to yourself what you would be; do what you gotta do; do well</p>
    <p>progress is wrecked or preserved by a single event</p>
    <p>can't steer unless already moving</p>
  </section>
  <section>
    {% for post in site.posts %}
    <article>
      <time datetime="{{ post.date | date: "%Y-%m-%d" }}">{{ post.date | date: "%Y-%m-%d" }}</time>
      <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
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
