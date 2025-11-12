const handleCopyClick = () => {
  const workflowTextarea = document.getElementById('workflow');
  const copyButton = document.getElementById('copyButton');
  const copyText = copyButton.querySelector('.copy-text');
  const copySuccess = copyButton.querySelector('.copy-success');
  
  if (!workflowTextarea || !copyButton) return;
  
  const textToCopy = workflowTextarea.value;
  
  navigator.clipboard.writeText(textToCopy).then(() => {
    copyText.style.display = 'none';
    copySuccess.style.display = 'inline';
    
    setTimeout(() => {
      copyText.style.display = 'inline';
      copySuccess.style.display = 'none';
    }, 2000);
  }).catch((err) => {
    console.error('Failed to copy text: ', err);
    workflowTextarea.select();
    document.execCommand('copy');
    copyText.style.display = 'none';
    copySuccess.style.display = 'inline';
    
    setTimeout(() => {
      copyText.style.display = 'inline';
      copySuccess.style.display = 'none';
    }, 2000);
  });
};

const handleCopyKeyDown = (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleCopyClick();
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const copyButton = document.getElementById('copyButton');
  
  if (copyButton) {
    copyButton.addEventListener('click', handleCopyClick);
    copyButton.addEventListener('keydown', handleCopyKeyDown);
  }
});

