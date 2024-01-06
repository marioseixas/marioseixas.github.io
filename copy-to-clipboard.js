document.addEventListener('DOMContentLoaded', function () {
  var highlightBlocks = document.querySelectorAll('pre.highlight, div.highlight');

  highlightBlocks.forEach(function(block) {
    var button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.title = 'Copy to clipboard';
    button.addEventListener('click', function () {
      // Now we have to find just the plain text within this code block without line numbers or other additions
      var code = block.querySelector('code').innerText;
      navigator.clipboard.writeText(code).then(function () {
        button.textContent = 'Copied!';
        setTimeout(function () { button.textContent = 'Copy'; }, 2000);
      }).catch(function (err) {
        console.error('Error copying text: ', err);
      });
    });

    block.appendChild(button);
  });
});
