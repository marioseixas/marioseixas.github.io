document.addEventListener('DOMContentLoaded', () => {
  const copyCodeButtons = document.querySelectorAll('.copy-code-button');
  const codeBlocks = document.querySelectorAll('.language-plaintext.highlighter-rouge pre code, .language-bash.highlighter-rouge pre code');

  copyCodeButtons.forEach((copyCodeButton, index) => {
    const code = codeBlocks[index].innerText;

    copyCodeButton.addEventListener('click', () => {
      // Copy the code to the user's clipboard
      window.navigator.clipboard.writeText(code).then(() => {
        // Update the button text visually
        const { innerText: originalText } = copyCodeButton;
        copyCodeButton.innerText = 'Copied!';

        // (Optional) Toggle a class for styling the button
        copyCodeButton.classList.add('copied');

        // After 2 seconds, reset the button to its initial UI
        setTimeout(() => {
          copyCodeButton.innerText = originalText;
          copyCodeButton.classList.remove('copied');
        }, 2000);
      }).catch(err => {
        console.error('Failed to copy: ', err);
      });
    });
  });
});
