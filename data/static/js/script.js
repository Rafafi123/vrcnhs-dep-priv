var message_timeout = document.getElementById("message-timer");


setTimeout(function() {
    messageTimeout.style.display = "none";
    messageTimeout.remove();  // Remove the element from the DOM
}, 9000);