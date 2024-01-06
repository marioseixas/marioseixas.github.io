document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.copy-button').forEach(function(button) {
    button.addEventListener('click', function() {
      const codeBlock = this.previousElementSibling.querySelector('code');
      const textToCopy = codeBlock.innerText.trim();
      navigator.clipboard.writeText(textToCopy).then(function() {
        // Optionally, provide visual feedback to the user here, e.g., changing the button text temporarily
        button.textContent = 'Copied!';
        setTimeout(function() { button.textContent = 'Copy'; }, 2000);
      }).catch(function(err) {
        console.error('Error copying text: ', err);
      });
    });
  });
});
