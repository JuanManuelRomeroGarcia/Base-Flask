var flashMessages = document.querySelectorAll('.flash-message');
flashMessages.forEach(function(message) {
    setTimeout(function() {
        message.style.opacity = 50;
        setTimeout(function() {
            message.remove();
        }, 1000);
    }, 10000);
});