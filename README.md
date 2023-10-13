<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Mario's blog where he shares his thoughts and archives.">
    <title>{{ site.title }}</title>
    <style>
        /* ... include all your CSS here ... */
    </style>
</head>
<body>
    <header>
        <ul>
            <li><a href="#home">Home</a></li>
            <li class="dropdown">
                <a href="javascript:void(0)" class="dropbtn">Menu</a>
                <div class="dropdown-content">
                    <a href="#">About</a>
                    <a href="#">Contact</a>
                </div>
            </li>
        </ul>
    </header>
    <main>
        <section id="home">
            <p class="quote"><a class="internal-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">Can't steer unless already moving</a></p>
        </section>
        <section>
            {% for post in site.posts %}
            <article>
                <time datetime="{{ post.date | date: '%Y-%m-%d' }}"> {{ post.date | date: "%Y-%m-%d" }}</time>
                <a href="{{ post.url | relative_url }}"> {{ post.title }} </a>
            </article>
            {% endfor %}
        </section>
        <section>
            <p class="quote">Progress is wrecked or preserved by a single event</p>
        </section>
    </main>
    <footer>
        <div id="contact-form">
            <form action="mailto:mario@email.com" method="post" enctype="text/plain">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="email">E-mail:</label><br>
                <input type="text" id="email" name="email"><br>
                <input type="submit" value="Send">
                <input type="reset" value="Reset">
            </form>
        </div>
        <p>&copy; 2023 Mario. All rights reserved.</p>
        <p>
            <a href="mailto:mario@email.com">Contact Me</a> | 
            <a href="https://twitter.com/mario">Twitter</a> | 
            <a href="https://linkedin.com/in/mario">LinkedIn</a>
        </p>
    </footer>
</body>
</html>
