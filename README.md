<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intentionally Blank</title>

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
@keyframes slideIn {
    from {transform: translateY(-100%);}
    to {transform: translateY(0);}
}
</style>
</head>
<body>
<main>
    <a class="internal-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">can't steer unless already moving</a>
    <section> 
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a href="{{ post.url }}"> {{ post.title }} </a>
        </article> 
        {% endfor %}
    </section>
</main>
</body>
</html>
