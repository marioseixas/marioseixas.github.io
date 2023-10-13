<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moving Elements</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background: #f2f2f2;
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
    </style>
  </head>
  <body>
    <main>
      <section>
        <p class="quote">Can't steer unless already moving</p>
      </section>
      <section>
        <p class="quote">Progress is wrecked or preserved by a single event</p>
      </section>
    </main>
  </body>
</html>
