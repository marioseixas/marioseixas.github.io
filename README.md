<style> 
    .quote { 
        text-align: center; 
        border: 1px solid black;
    } 
</style>
<main>
    <section><p class="quote"><a class="internal-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">can't steer unless already moving</a></p></section>
    <section> 
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a href="{{ post.url }}"> {{ post.title }} </a>
        </article> 
        {% endfor %}
    </section>
    <section><p class="quote">progress is wrecked or preserved by a single event</p></section>
</main>
