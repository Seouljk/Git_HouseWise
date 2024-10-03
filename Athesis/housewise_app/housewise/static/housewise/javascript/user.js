function redirectToMenu() {
    const username = "{{ user.username }}"; // Ensure this variable is correctly set
    console.log("Redirecting to menu for user:", username);
    window.location.href = `/housewise/${username}/menu/`; // Ensure trailing slash
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

function showUserInfo(user_id, name, age, username, hashedPassword, email) {
    // Update the span elements with user info
    document.getElementById('user-id').textContent = user_id;
    document.getElementById('user-name').textContent = name;
    document.getElementById('user-age').textContent = age;
    document.getElementById('user-username').textContent = username;
    document.getElementById('user-password').textContent = '****************';
    document.getElementById('user-email').textContent = email;

    // Fetch and display login sessions
    fetchLoginSessions(user_id);
}

function fetchLoginSessions(user_id) {
    fetch(`/housewise/user_login_sessions?user_id=${user_id}`) // Adjust the URL based on your routing
        .then(response => response.json())
        .then(data => {
            const logEntriesDiv = document.querySelector('.log-entries');
            logEntriesDiv.innerHTML = ''; // Clear previous entries

            if (data.sessions.length === 0) {
                logEntriesDiv.innerHTML = '<div class="log-entry">No login logs available.</div>';
                return;
            }

            data.sessions.forEach(session => {
                const logEntry = document.createElement('div');
                logEntry.classList.add('log-entry');
                logEntry.innerHTML = `
                    <p><strong>Login Date & Time:</strong> ${new Date(session.login_time).toLocaleString()}</p>
                    <p><strong>Duration:</strong> ${session.login_duration ? session.login_duration : 'Still logged in'}</p>
                `;
                logEntriesDiv.appendChild(logEntry);
            });
        })
        .catch(error => {
            console.error('Error fetching login sessions:', error);
        });
}