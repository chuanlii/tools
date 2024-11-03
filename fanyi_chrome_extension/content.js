var translateText = ''
document.addEventListener('mouseup', () => {
  const selectText = window.getSelection().toString().trim();
  if (selectText !== '') {
    translateText = selectText 
    console.log("show btn ", translateText)
    showTranslateButton();
  } else {
    console.log("hide btn ", translateText)
    hideTranslateButton();
  }
});



function showTranslateButton() {
  let translateButton = document.getElementById('translateButton');
  if (!translateButton) {
    translateButton = document.createElement('div');
    translateButton.id = 'translateButton';
    translateButton.innerText = '翻译';
    translateButton.style.cssText = `
        position: absolute;
        background-color: #4CAF50;
        color: white;
        padding: 5px;
        border-radius: 5px;
        cursor: pointer;
        z-index: 10000;
        font-size: 12px;
      `;
    document.body.appendChild(translateButton);

    translateButton.addEventListener('click', () => {
      console.log('Sending message to background script:', translateText);
      t = { "type": 'translate', "words": translateText }
      chrome.runtime.sendMessage(t);
    });
  }

  const { x, y } = window.getSelection().getRangeAt(0).getBoundingClientRect();
  translateButton.style.top = `${window.scrollY + y + 10}px`;
  translateButton.style.left = `${window.scrollX + x}px`;
  translateButton.style.display = 'block';
}

function hideTranslateButton() {
  const translateButton = document.getElementById('translateButton');
  if (translateButton !== '') {
    translateButton.style.display = 'none';
  }
};


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'showTranslation') {
    alert(`翻译结果：${request.translation}`);
  }
  return true
});
