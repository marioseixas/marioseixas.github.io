<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Mario's blog where he shares his thoughts and archives.">
    <title>Mario's Blog</title>
    <style>
        /* CSS codes for styling each element */
        body {
            font-family: Arial, sans-serif;
        }
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #333;
        }
        li {
            float: left;
        }
        li a, .dropbtn {
            display: inline-block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
        li a:hover, .dropdown:hover .dropbtn {
            background-color: red;
        }
        li.dropdown {
            display: inline-block;
        }
        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            min-width: 160px;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        }
        .dropdown-content a {
            color: black;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            text-align: left;
        }
        .dropdown-content a:hover {background-color: #f1f1f1;}
        .dropdown:hover .dropdown-content {
            display: block;
        }
        article { 
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .quote { 
            text-align: center; 
            border: 1px solid black;
            padding: 20px;
            margin: 20px auto;
            animation: glow 2s ease-in-out infinite;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px #ffcccc, 0 0 10px #ffcccc, 0 0 15px #ffcccc, 0 0 20px #ffcccc; }
            100% { box-shadow: 0 0 10px #ffcccc, 0 0 15px #ffcccc; }
        }
        /* Styles for Contact form */
        #contact-form {
            text-align: center;
            padding: 20px;
        }
        #contact-form input[type=text], #contact-form input[type=email] {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        #contact-form input[type=submit] {
            background-color: #4CAF50; // You can custom this
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        #contact-form input[type=submit]:hover {
            opacity: 0.8;
        }
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
                <a href="{{ post.url }}"> {{ post.title }} </a>
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
