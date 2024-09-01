document.addEventListener('DOMContentLoaded', () => {
  let codeBlocks = document.querySelectorAll(".code-block code");

  codeBlocks.forEach((codeBlock) => {
    const copyBtn = document.createElement("button");
    copyBtn.innerText = "Copy";
    copyBtn.style.marginLeft = "10px";
    copyBtn.addEventListener("click", async () => {
      await copyCode(codeBlock);
      showSnackbar();
    });
    codeBlock.parentNode.insertBefore(copyBtn, codeBlock.nextSibling);
  });

  async function copyCode(codeBlock) {
    try {
      await navigator.clipboard.writeText(codeBlock.innerText);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  }

  function showSnackbar() {
    let snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    setTimeout(() => { snackbar.className = snackbar.className.replace("show", ""); }, 3000);
  }
});
