document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('pre code').forEach((codeBlock) => {
    // Check if the code block is inside a Liquid block
    if (codeBlock.closest('.liquid-block')) {
      return; // Skip this code block
    }

    const button = document.createElement('button');
    button.className = 'copy-button';
    button.type = 'button';
    button.innerText = 'Copy';

    button.addEventListener('click', () => {
      const code = codeBlock.innerText;
      navigator.clipboard.writeText(code).then(() => {
        button.innerText = 'Copied!';
        setTimeout(() => {
          button.innerText = 'Copy';
        }, 2000);
      }).catch((err) => {
        console.error('Failed to copy text: ', err);
      });
    });

    const pre = codeBlock.parentNode;
    if (pre && pre.tagName === 'PRE') {
      pre.insertBefore(button, codeBlock);
    }
  });
});
