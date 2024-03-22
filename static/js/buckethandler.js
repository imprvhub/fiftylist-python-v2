var canClick = true; 

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("bucketButton").addEventListener("click", function(event) {
        if (!canClick) return; 
        
        event.preventDefault(); 

        canClick = false;
        
        var htmlContent = document.documentElement.outerHTML;
        var excludedScriptLine = '<script src="/static/js/buckethandler.js"></script>';
        htmlContent = htmlContent.replace(excludedScriptLine, '');
        var normalizedHtmlContent = normalizeHtml(htmlContent);
        var tempContainer = document.createElement('div');
        tempContainer.innerHTML = normalizedHtmlContent;
        var shareContainer = tempContainer.querySelector('.share-container');
        if (shareContainer) {
            shareContainer.style.display = 'flex';
        }

        var modifiedHtmlContent = tempContainer.innerHTML;
        normalizedHtmlContent = modifiedHtmlContent;
        var userInput = document.querySelector('input');
        var userInputValue = userInput.value.trim();
        var dynamicTextDiv = document.createElement('div');
        dynamicTextDiv.className = 'dynamic-text';
        if (userInputValue !== '') { 
            dynamicTextDiv.textContent = '"' + userInputValue + '"'; 
        }
        userInput.parentNode.insertBefore(dynamicTextDiv, userInput.nextSibling);
        userInput.style.display = 'none';
        var inputInfo = document.querySelector('.input-info');
        inputInfo.style.display = 'none';
        var normalizedHtmlContent = document.documentElement.outerHTML;
        normalizedHtmlContent = normalizedHtmlContent.replace(userInput.outerHTML, '');
        normalizedHtmlContent = normalizedHtmlContent.replace(inputInfo.outerHTML, '');
        document.getElementById("bucketButton").style.display = "none";
        var userInputParent = userInput.parentNode;
        userInputParent.insertBefore(dynamicTextDiv, userInput.nextSibling);
    
        fetch('/generate_short_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain' 
            },
            body: normalizedHtmlContent
        })
        .then(response => response.text()) 
        .then(data => {
            var shortUrl = data; 
            window.location.href = "/shared/" + shortUrl;
            document.getElementById("shortLinkButton").style.display = "inline-block";
            canClick = true;
        })
        .catch(error => {
            console.error('Error:', error);
            canClick = true; 
        });
    });
});

function normalizeHtml(html) {
    return html.normalize('NFD').replace(/[\u0300-\u036f]/g, "");
}
