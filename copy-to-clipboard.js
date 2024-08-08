document.addEventListener('DOMContentLoaded', () => {
  const copyButtons = document.querySelectorAll('.copy-button');

  copyButtons.forEach(button => {
    button.addEventListener('click', () => {
      const codeBlock = button.closest('pre > code');
      if (!codeBlock) return;

      const codeText = codeBlock.textContent.trim();
      copyToClipboard(codeText)
        .then(() => {
          button.classList.add('copied');
          button.textContent = 'Copied!';

          setTimeout(() => {
            button.classList.remove('copied');
            button.textContent = 'Copy';
          }, 2000);
        })
        .catch(err => console.error('Failed to copy text: ', err));
    });
  });
});

async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Async: Could not copy text: ', err);
    // Fallback for older browsers
    await fallbackCopyToClipboard(text);
  }
}

function fallbackCopyToClipboard(text) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';  // Prevent scrolling to bottom
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  return new Promise((resolve, reject) => {
    try {
      const successful = document.execCommand('copy');
      resolve();
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
      reject(err);
    }
    document.body.removeChild(textArea);
  });
}
