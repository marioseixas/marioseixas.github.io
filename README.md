<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Intentionally Blank</title>
<style>
body {
    font-family: Arial, sans-serif;
    color: #ffffff; /* Changes font color to white for readability */
    background: #000000; /* Changes background to black as requested */
}

main {
    margin-top: 10vh;
    animation: fadeIn 2s ease;
}

search-link {
    display: block; /* Allows setting of width */
    text-align: right; /* Aligns SEARCH link to the right */
    border: 1px solid #ffffff; /* Adds border around SEARCH link */
    color: #33ccff; /* Changes SEARCH link color for readability on black background */
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

section {
    margin: 5vh auto;
    padding:5vh;
    background: #000000;
    color: #ffffff; /* Changes section font color to white for readability */
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

.search-link {
    text-align: right; /* Aligns the SEARCH link to the right */
    border: 1px solid #33ccff; /* Gives the link a border */
}
</style>
</head>
<body>
<main>
    <section>        
        <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
        {% for post in site.posts %} 
            <article>
                <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
                <a href="{{ post.url }}" style="color: #33ccff;"> {{ post.title }} </a>
            </article> 
        {% endfor %}
    </section>
</main>
</body>
</html>
