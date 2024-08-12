document.addEventListener('DOMContentLoaded', () => {
  const copyButtons = document.querySelectorAll('.copy-code-button');

  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const codeBlockId = button.dataset.codeTarget;
      const codeBlock = document.getElementById(codeBlockId)?.querySelector('pre code');
      if (!codeBlock) {
        console.error('Code block not found.');
        return;
      }

      const codeText = codeBlock.textContent.trim();
      try {
        await navigator.clipboard.writeText(codeText);
        // Optionally provide visual feedback to the user
        button.textContent = 'Copied!';
        setTimeout(() => {
          button.textContent = 'Copy';
        }, 2000);
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    });
  });
});
