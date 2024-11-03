chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log("recv ", request.words)
    if (request.type === 'translate') {
        fetch(`http://localhost:5000/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "text": request.words
            })
        })
            .then(response => {
                return response.json()
            })
            .then(resp => {
                console.log("resp ", resp)
                chrome.tabs.sendMessage(sender.tab.id, { type: 'showTranslation', translation: resp.data });
            })
            .catch(error => console.error('Error:', error));
    }
    return true
});
