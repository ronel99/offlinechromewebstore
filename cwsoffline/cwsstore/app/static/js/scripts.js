// This file contains JavaScript code for client-side functionality, such as handling user interactions.

document.addEventListener("DOMContentLoaded", function() {
    const downloadButtons = document.querySelectorAll(".download-button");

    downloadButtons.forEach(button => {
        button.addEventListener("click", function() {
            const extensionId = this.dataset.extensionId;
            window.location.href = `/download/${extensionId}`;
        });
    });
});