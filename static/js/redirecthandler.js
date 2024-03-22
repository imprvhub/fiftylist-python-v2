let definitiveUrl = ''; 

document.getElementById("shortLinkButton").addEventListener("click", function(event) {
    event.preventDefault(); 
    if (definitiveUrl) {
        openUrlInNewTab(definitiveUrl);
    } else {
        getShortUrlFromPython();
    }
});

function getShortUrlFromPython() {
    fetch('/definitive_url_handler', {
        method: 'GET'
    })
    .then(response => response.json()) 
    .then(data => {
        definitiveUrl = data.definitive_url;
        const button = document.getElementById("shortLinkButton");
        button.textContent = definitiveUrl ? '' + definitiveUrl : 'Create FiftyCard Link';
        button.style.color = '#18EE90';
        button.style.display = 'inline-block'; 
        const shareContainer = document.querySelector('.share-container');
        shareContainer.style.display = 'flex';
        const copyIcon = document.getElementById('copy');
        const openIcon = document.getElementById('open');
        const telegramIcon = document.getElementById('telegram');
        const facebookIcon = document.getElementById('facebook');
        const whatsappIcon = document.getElementById('whatsapp');
        const twitterIcon = document.getElementById('twitter');
        const redditIcon = document.getElementById('reddit');
        const emailIcon = document.getElementById('mail');

        const title = 'Check out this amazing Fifty Card!';
        const description = 'This Fifty Card was generated dynamically from Spotify API and I wanted to share it with you!';

        function copyUrlToClipboard() {
            navigator.clipboard.writeText(definitiveUrl)
                .then(() => {
                    alert("URL copiada al portapapeles: " + definitiveUrl);
                })
                .catch(err => {
                    console.error('Error al copiar al portapapeles: ', err);
                });
        }

        function openInNewTab() {
            window.open(definitiveUrl, '_blank');
        }

        function shareOnTelegram() {
            const telegramUrl = 'https://t.me/share/url?url=' + encodeURIComponent(definitiveUrl) + '&text=' + encodeURIComponent(description);
            window.open(telegramUrl, '_blank');
        }


        function shareOnFacebook() {
            const facebookUrl = 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(definitiveUrl);
            window.open(facebookUrl, '_blank');
        }

        function shareOnWhatsApp() {
            const whatsappUrl = 'whatsapp://send?text=' + encodeURIComponent(definitiveUrl);
            window.open(whatsappUrl);
        }

        function shareOnTwitter() {
            const twitterUrl = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(definitiveUrl) + '&title=' + encodeURIComponent(title);
            window.open(twitterUrl, '_blank');
        }

        function shareOnReddit() {
            const redditUrl = 'https://www.reddit.com/submit?url=' + encodeURIComponent(definitiveUrl) + '&title=' + encodeURIComponent(title);
            window.open(redditUrl, '_blank');
        }
        
        function shareViaEmail() {
            const subject = 'Check out this amazing Fifty Card!';
            const emailBody = 'This Fifty Card was generated dynamically from Spotify  API and I wanted to share it with you! ' + definitiveUrl;
            const emailUrl = 'mailto:?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(emailBody);
            window.open(emailUrl);
        }
        
        openIcon.addEventListener('click', openInNewTab);
        copyIcon.addEventListener('click', copyUrlToClipboard);
        telegramIcon.addEventListener('click', shareOnTelegram);
        facebookIcon.addEventListener('click', shareOnFacebook);
        whatsappIcon.addEventListener('click', shareOnWhatsApp);
        twitterIcon.addEventListener('click', shareOnTwitter);
        redditIcon.addEventListener('click', shareOnReddit);
        emailIcon.addEventListener('click', shareViaEmail);
    })
    .catch(error => {
        console.error('Error while getting the definitive URL generated in Python:', error);
    });
}

function openUrlInNewTab(url) {
    window.open(url, '_blank');
}
