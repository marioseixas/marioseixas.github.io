// copy-to-clipboard.js
document.addEventListener('DOMContentLoaded', function () {
  var copyButtons = document.querySelectorAll('.copy-button');
  copyButtons.forEach(function(button) {
    button.addEventListener('click', function () {
      var code = button.previousElementSibling.innerText;
      navigator.clipboard.writeText(code).then(function () {
        button.textContent = '!';
        setTimeout(function() {
          button.textContent = '&copy;';
        }, 2000);
      }).catch(function() {
        button.textContent = 'Error';
      });
    });
  });
});
