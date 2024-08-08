document.addEventListener('DOMContentLoaded', () => {
  const copyButtons = document.querySelectorAll('.copy-button');

  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const codeBlock = button.closest('.code-container')?.querySelector('pre code');
      if (!codeBlock) {
        console.error('Code block not found.');
        return;
      }

      const codeText = codeBlock.textContent.trim();
      try {
        await copyToClipboard(codeText);
        showCopySuccess(button);
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    });
  });
});

async function copyToClipboard(text) {
  if (navigator.clipboard) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Async: Could not copy text: ', err);
      await fallbackCopyToClipboard(text);
    }
  } else {
    await fallbackCopyToClipboard(text);
  }
}

function fallbackCopyToClipboard(text) {
  return new Promise((resolve, reject) => {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';  // Prevent scrolling to bottom
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      if (successful) {
        resolve();
      } else {
        reject(new Error('Fallback: Copy command was unsuccessful'));
      }
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
      reject(err);
    } finally {
      document.body.removeChild(textArea);
    }
  });
}

function showCopySuccess(button) {
  button.classList.add('copied');
  button.textContent = 'Copied!';

  setTimeout(() => {
    button.classList.remove('copied');
    button.textContent = 'Copy';
  }, 2000);
}
