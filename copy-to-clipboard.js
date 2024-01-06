document.querySelectorAll('.copy-button').forEach(function(button) {
  button.addEventListener('click', function() {
    // Find the parent .code-container then find the contained <code>
    var codeContainer = this.closest('.code-container');
    var codeBlock = codeContainer ? codeContainer.querySelector('code') : null;
    if (codeBlock) {
      // Now we have a reference to the <code>, continue as before
      var textToCopy = codeBlock.innerText.trim();
      navigator.clipboard.writeText(textToCopy).then(function() {
        button.textContent = 'Copied!';
        setTimeout(function() { button.textContent = 'Copy'; }, 2000);
      }).catch(function(err) {
        console.error('Error copying text: ', err);
      });
    } else {
      console.error("Couldn't find the code block associated with the copy button.");
    }
  });
});
