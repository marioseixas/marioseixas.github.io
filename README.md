<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<div class="header-container">
  <title>Intent &#8660; Break</title>
  <div id="google-search-box" class="search-box">
    <div class="gcse-search"></div>
  </div>
</div>

<style>
  body {
    background: #000000; /* Changes background to black */
    color: #ffffff; /* Fonts color changed to white */
  }

  main {
    margin-top: 10vh;
    animation: fadeIn 2s ease;
  }

  @keyframes fadeIn {
      from {opacity: 0;}
      to {opacity: 1;}
  }

  @media (max-width: 600px) {
    .header-container {
      flex-direction: column;
    }
    .search-box {
      width: 100%;
      max-width: none; /* Allows it to take the full width on smaller screens */
      margin-top: 10px; /* Optional: adds some space between the title and search box */
    }
  }
  
  pre, code {
    word-wrap: break-word;
  }

  section {
    margin: 5vh auto;
    padding:5vh;
    background: #343434; 
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
    display: inline-block; /* Makes the link behave like a block */
    margin-bottom: 1em; /* Gives some space below the link */
    padding: 0.5em; /* Gives some padding inside the box */
    color: #ff8000; /* Thermatic color of the text LINK */
    border: 1px solid #ff8000; /* Border color same as the link */
    float: right; /* Floats the box to right */  
  }
</style>

<script async src="https://cse.google.com/cse.js?cx=000547254117280036387:qwl-zdl2sn0"></script>
</head>
<body>
<main>
    <section>
    <a href="https://ib.bsb.br/404.html" style="text-align: center; display: block;">can't steer unless already moving</a>
    <a class="search-link" href="https://github.com/search?q=repo%3Amarioseixas%2Fmarioseixas.github.io">SEARCH</a>
        {% for post in site.posts %} 
        <article>
            <time datetime="{{ post.date | date: "%Y-%m-%d" }}"> {{ post.date | date: "%Y-%m-%d" }} </time>
            <a style="color:#33ccff;" href="{{ post.url }}"> {{ post.title }} </a> <!-- Changes post title color for readability -->
        </article> 
        {% endfor %}
    </section>
</main>
</body>
</html>
