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
    const feedbackModal = document.getElementById('feedbackModal');
    feedbackModal.style.display = 'block';
}

function closeFeedbackModal() {
    const feedbackModal = document.getElementById('feedbackModal');
    feedbackModal.style.display = 'none';
}


function showUserInfo(userId, name, age, username, password, email) {

    const userInfo = document.getElementById('user-info');
    const defaultMessage = document.getElementById('default-message');
    const userDetails = document.getElementById('user-details');

    // Update user details
    document.getElementById('user-id').textContent = userId;
    document.getElementById('user-name').textContent = name;
    document.getElementById('user-age').textContent = age;
    document.getElementById('user-username').textContent = username;
    document.getElementById('user-password').textContent = '****************';
    document.getElementById('user-email').textContent = email;

    // Fetch login session data via AJAX
    fetch(`/housewise/login_sessions/?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            const logEntriesContainer = document.getElementById('log-entries');
            logEntriesContainer.innerHTML = ""; // Clear previous logs

            if (data.login_sessions && data.login_sessions.length > 0) {
                data.login_sessions.forEach(session => {
                    const logEntry = document.createElement('div');
                    logEntry.classList.add('log-entry');
                    logEntry.innerHTML = `
                        <p><strong>Login Time:</strong> ${session.login_time}</p>
                        <p><strong>Logout Time:</strong> ${session.logout_time}</p>
                        <p><strong>Duration:</strong> ${session.duration}</p>
                        <p><strong>Active:</strong> ${session.is_active ? 'Yes' : 'No'}</p>
                        <hr>
                    `;
                    logEntriesContainer.appendChild(logEntry);
                });
            } else {
                logEntriesContainer.innerHTML = "<p>No login sessions found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching login sessions:", error);
            document.getElementById('log-entries').innerHTML = "<p>Error loading login sessions.</p>";
        });

    // Fetch feedback data via AJAX
    fetch(`/housewise/user_feedbacks/?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            const feedbackContent = document.getElementById('feedback-content'); // The modal content container
            feedbackContent.innerHTML = ""; // Clear previous feedbacks

            if (data.feedbacks && data.feedbacks.length > 0) {
                data.feedbacks.forEach(feedback => {
                    const feedbackItem = document.createElement('div');
                    feedbackItem.classList.add('feedback-item');
                    feedbackItem.innerHTML = `
                        <p><strong>Project Name:</strong> ${feedback.project_name}</p>
                        <p><strong>Project Created:</strong> ${feedback.project_created}</p>
                        <p><strong>Rating:</strong> ${feedback.rating}</p>
                        <p><strong>Description:</strong> ${feedback.description}</p>
                        <p><strong>Feedback Date:</strong> ${feedback.feedback_datetime}</p>
                        <hr>
                    `;
                    feedbackContent.appendChild(feedbackItem);
                });
            } else {
                feedbackContent.innerHTML = "<p>No feedbacks found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching feedbacks:", error);
            document.getElementById('feedback-content').innerHTML = "<p>Error loading feedbacks.</p>";
        });

    // Hide the default message and show user details
    defaultMessage.style.display = 'none';
    userDetails.style.display = 'block';
    userInfo.setAttribute('data-default', 'false');
}


function resetUserInfo() {
    const userInfo = document.getElementById('user-info');
    const defaultMessage = document.getElementById('default-message');
    const userDetails = document.getElementById('user-details');

    // Clear user details
    document.getElementById('user-id').textContent = '';
    document.getElementById('user-name').textContent = '';
    document.getElementById('user-age').textContent = '';
    document.getElementById('user-username').textContent = '';
    document.getElementById('user-password').textContent = '';
    document.getElementById('user-email').textContent = '';
    document.getElementById('log-entries').innerHTML = '';

    // Show the default message and hide user details
    defaultMessage.style.display = 'block';
    userDetails.style.display = 'none';
    userInfo.setAttribute('data-default', 'true');
}


async function fetchDashboardDataAndRenderChart() {
    try {
        const response = await fetch('/housewise/api/dashboard-data/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const { total_users, total_users_logged_in, total_users_not_logged_in, total_feedbacks } = data;

        document.getElementById('total-users-logged-in').querySelector('h3').textContent = data.total_users_logged_in;
        document.getElementById('total-users').querySelector('h3').textContent = data.total_users;
        document.getElementById('total-feedbacks').textContent = total_feedbacks;

        // Extract data for the donut chart

        // Render the Donut Chart
        const ctx = document.getElementById('userDonutChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Logged In', 'Not Logged In'],
                datasets: [{
                    label: 'User Distribution',
                    data: [total_users_logged_in, total_users_not_logged_in],
                    backgroundColor: ['#4CAF50', '#FFC107'], // Colors for sections
                    hoverBackgroundColor: ['#45A049', '#FFCA28']
                }]
            },
            options: {
                responsive: true,
                plugins: {  
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                const label = tooltipItem.label || '';
                                const value = tooltipItem.raw;
                                const total = total_users;
                                const percentage = ((value / total) * 100).toFixed(2);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', fetchDashboardDataAndRenderChart);


