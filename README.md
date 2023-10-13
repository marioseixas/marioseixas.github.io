<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Mario's blog where he shares his thoughts and archives.">
    <title>Mario's Blog</title>
    <style> 
        .quote { 
            text-align: center; 
            border: 1px solid black;
            padding: 20px;
            margin: 20px auto;
        }
        article { 
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        time {
            margin-right: 10px;
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
        <section>
            <p class="quote">
                <a class="internal-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">
                    Can't steer unless already moving
                </a>
            </p>
        </section>
        <section>
            {% for post in site.posts %} 
            <article>
                <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
                <a href="{{ post.url }}"> {{ post.title }} </a>
            </article> 
            {% endfor %}
        </section>
        <section>
            <p class="quote">
                Progress is wrecked or preserved by a single event
            </p>
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
