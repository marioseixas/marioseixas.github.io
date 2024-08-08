document.addEventListener('DOMContentLoaded', () => {
  const copyButtons = document.querySelectorAll('.copy-button');

  copyButtons.forEach(button => {
    button.addEventListener('click', () => {
      const codeBlock = button.closest('pre');
      if (!codeBlock) return;

      const codeText = codeBlock.innerText.trim();
      copyToClipboard(codeText)
        .then(() => {
          button.classList.add('copied');
          button.innerText = 'Copied!';

          setTimeout(() => {
            button.classList.remove('copied');
            button.innerText = 'Copy';
          }, 2000);
        })
        .catch(err => console.error('Failed to copy text: ', err));
    });
  });
});

function copyToClipboard(text) {
  return navigator.clipboard.writeText(text).catch(err => {
    console.error('Async: Could not copy text: ', err);
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';  // Prevent scrolling to bottom
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    }
    document.body.removeChild(textArea);
  });
}
