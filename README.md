<div>
  <div style="margin:3em 0 2em;">
    {% for post in site.posts %}
    <div class="list-entry">
      <span class="faded">{{ post.date | date: "%Y-%m-%d" }}</span>
      <br>
      <a class="internal-link" href="{{ post.url }}">{{ post.title }}</a>
    </div>
    {% endfor %}
  </div>
  <p>
    <a title='GitHub' target="_blank" rel="noreferrer" href="https://github.com/marioseixas/marioseixas.github.io">
      GitHub
    </a>
  </p>
</div>
