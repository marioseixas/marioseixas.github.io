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
    margin: 0;
    padding: 0;
    background: #f2f2f2;
}
header {
    background: #333;
    color: #f2f2f2;
    padding: 10px 0;
    position: fixed;
    width: 100%;
    transition: all 0.3s ease;
}
nav ul {
    padding: 0;
    margin: 0;
    list-style: none;
    display: flex;
    justify-content: space-around;
}
nav a {
    color: #f2f2f2;
    text-decoration: none;
}
main {
    margin-top: 50px;
    animation: fadeIn 2s ease;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
section {
    text-align: center;
    margin: 20px 0;
    padding: 20px;
    background: #e2e2e2;
    border-radius: 10px;
    transform: rotate(-1deg);
    transition: transform 1s ease;
}
section:hover {
    transform: rotate(1deg);
}
.quote { 
    text-align: center; 
    border: 1px solid black;
    padding: 20px;
    margin: 20px auto;
    animation: slideIn 1s ease;
}
@keyframes slideIn {
    from {transform: translateY(-100%);}
    to {transform: translateY(0);}
}
footer {
    background: #333;
    color: #f2f2f2;
    padding: 10px 0;
    text-align: center;
    position: fixed;
    width: 100%;
    bottom: 0;
    transition: all 0.3s ease;
}
</style>
</head>
<body>
<header>
    <nav>
        <ul>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
</header>
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
<footer>
    <p>&copy; 2023 Mario. All rights reserved.</p>
    <p>
        <a href="mailto:mario@email.com">Contact Me</a> |
        <a href="https://twitter.com/mario">Twitter</a> |
        <a href="https://linkedin.com/in/mario">LinkedIn</a>
    </p>
</footer>
</body>
</html>
