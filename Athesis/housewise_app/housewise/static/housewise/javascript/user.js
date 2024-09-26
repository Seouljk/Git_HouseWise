
function redirectToMenu() {
    // Redirect to the menu page
    window.location.href = "/housewise/menu";
}

// Close the modal if the user clicks anywhere outside the modal content
window.onclick = function(event) {
    var modal = document.getElementById('feedbackModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
    console.log("Feedback modal opened");
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
    console.log("Feedback modal closed");
}
