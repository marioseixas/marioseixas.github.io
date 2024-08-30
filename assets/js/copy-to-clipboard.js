document.addEventListener('DOMContentLoaded', function () {
  var highlightBlocks = document.querySelectorAll('pre[class^='language-']');
  highlightBlocks.forEach(function(block) {
    var button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.title = 'Copy to clipboard';
    button.addEventListener('click', function () {
      // Find the plain text within this code block without line numbers or other additions
      var code = block.querySelector('code').innerText;
      navigator.clipboard.writeText(code).then(function () {
        button.textContent = 'Copied!';
        setTimeout(function() {
          button.textContent = 'Copy';
        }, 2000);
      }).catch(function() {
        button.textContent = 'Error';
      });
    });
    // Prepend the button to the code block
    block.insertBefore(button, block.firstChild);
  });
});
