<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Mario's blog where he shares his thoughts and archives.">
<title>Mario's Blog</title>

<!-- Inline styles for complex transformations and animations -->
<style>
body {
    font-family: Arial, sans-serif;
    background: #f2f2f2;
}
main {
    margin-top: 10vh;
    animation: fadeIn 2s ease;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
section {
    text-align: center;
    margin: 5vh auto;
    padding:5vh;
    background: #e2e2e2;
    border-radius: 1em;
    transform: rotate(-1deg);
    transition: transform 1s ease;
}
section:hover {
    transform: rotate(1deg);
}
.quote { 
    text-align: center; 
    border: 1px solid black;
    padding: 5vh;
    margin: 5vh auto;
    animation: slideIn 1s ease;
}
@keyframes slideIn {
    from {transform: translateY(-100%);}
    to {transform: translateY(0);}
}
</style>
</head>
<body>
<main>
    <section id="about">
        <p class="quote">Can't steer unless already moving</p>
    </section>
    <section> 
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a href="{{ post.url }}"> {{ post.title }} </a>
        </article> 
        {% endfor %}
    </section>
    <section id="contact">
        <p class="quote">Progress is wrecked or preserved by a single event</p>
    </section>
</main>
</body>
</html>
