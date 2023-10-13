<style> 
    .quote { 
        text-align: center; 
        border: 1px solid black;
    } 
</style>
<main>
    <section><p class="quote">can't steer unless already moving</p></section>
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
