function redirectToLogout() {
    fetch("/housewise/logout/", {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        credentials: "same-origin"
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Logged out successfully') {
            // Redirect to the login page
            window.location.href = "/housewise/";
            history.replaceState(null, null, "/housewise/");
        }
    })
    .catch(error => {
        console.error("Error logging out:", error);
    });
}

// Helper function to get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}


function redirectToProfile() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    if (username) {
        window.location.href = `/housewise/${username}/profile/`;
    } else {
        console.error("Username not found!");
    }
}