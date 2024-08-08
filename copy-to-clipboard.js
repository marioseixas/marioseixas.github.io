// copy-to-clipboard.js
document.addEventListener('DOMContentLoaded', function () {
  var highlightBlocks = document.querySelectorAll('div.code-container');
  highlightBlocks.forEach(function(block) {
    var button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.title = 'Copy to clipboard';
    button.addEventListener('click', function () {
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
    block.appendChild(button);
  });
});
