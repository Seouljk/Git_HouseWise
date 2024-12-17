function redirectToMenu() {
    const username = "{{ user.username }}"; // Ensure this variable is correctly set
    console.log("Redirecting to menu for user:", username);
    window.location.href = `/housewise/${username}/menu/`; // Ensure trailing slash
}

function redirectToUserMenu(button) {
    const userId = button.getAttribute('data-user-id'); // Extract user ID
    const adminUsername = button.getAttribute('data-admin-username'); // Extract admin username
    console.log("Redirect Button Clicked. User ID:", userId, "Admin Username:", adminUsername);

    if (userId && adminUsername) {
        // Redirect to the user menu with the selected_id parameter
        window.location.href = `/housewise/${adminUsername}/menu/user/?selected_id=${userId}`;
    } else {
        console.error('User ID or Admin Username is missing for redirection.');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const feedbackButton = document.getElementById('feedback-username-btn');
    if (feedbackButton) {
        feedbackButton.addEventListener('click', function () {
            console.log('Feedback Button Clicked');
        });
    } else {
        console.error('Feedback Button not found.');
    }
});

async function fetchFeedbacks() {
    try {
        const response = await fetch('/housewise/api/feedbacks/'); // Absolute path
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const feedbackList = document.getElementById('feedback-list');
        feedbackList.innerHTML = ""; // Clear placeholder

        data.feedbacks.forEach(feedback => {
            const feedbackItem = document.createElement('li');
            feedbackItem.classList.add('feedback-item');
            feedbackItem.innerHTML = `
                <button class="feedback-button" onclick="showFeedbackDetails(${feedback.feedback_id})">
                    <strong>${feedback.project_name}</strong>
                    <span class="stars">${generateStars(feedback.rating)}</span>
                </button>
                <div class="feedback-user">
                    <i class="fa-regular fa-user"></i> ${feedback.user}
                </div>
            `;
            feedbackList.appendChild(feedbackItem);
        });
    } catch (error) {
        console.error('Error fetching feedbacks:', error);
    }
}

// Generate star rating HTML
function generateStars(rating) {
    const maxStars = 5;
    let stars = '';
    for (let i = 1; i <= maxStars; i++) {
        stars += i <= rating
            ? '<i class="fas fa-star"></i>' // Filled star
            : '<i class="far fa-star"></i>'; // Empty star
    }
    return stars;
}

async function showFeedbackDetails(feedbackId) {
    try {
        const response = await fetch('/housewise/api/feedbacks/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const feedback = data.feedbacks.find(f => f.feedback_id === feedbackId);

        if (feedback) {
            document.getElementById('feedback-id').textContent = feedback.feedback_id;
            document.getElementById('project-name').textContent = feedback.project_name;
            document.getElementById('rating').innerHTML = generateStars(feedback.rating);
            document.getElementById('feedback-datetime').textContent = feedback.feedback_datetime;
            document.getElementById('description').textContent = feedback.description;

            // Replace text in the feedback button with the username
            const feedbackButton = document.getElementById('feedback-username-btn');
            feedbackButton.textContent = feedback.user;

            // Dynamically set data-user-id
            feedbackButton.setAttribute('data-user-id', feedback.feedback_id); // Or use the correct user_id if available

            // Show feedback details section
            document.getElementById('default-message').style.display = 'none';
            document.getElementById('feedback-details').style.display = 'block';
        }
    } catch (error) {
        console.error('Error fetching feedback details:', error);
    }
}

// Call fetchFeedbacks on page load
document.addEventListener('DOMContentLoaded', fetchFeedbacks);

async function fetchGraphDataAndRenderChart() {
    try {
        const response = await fetch('/housewise/api/graph-data/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Update the DOM with values
        document.getElementById('total-projects').querySelector('h3').textContent = data.total_projects;
        document.getElementById('total-projects-rated').querySelector('h3').textContent = data.total_projects_rated;
        document.getElementById('average-rating').textContent = data.average_rating;

        // Render the Donut Chart
        const ctx = document.getElementById('userDonutChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Total Projects', 'Rated Projects'],
                datasets: [
                    {
                        label: 'Projects Distribution',
                        data: [data.total_projects, data.total_projects_rated],
                        backgroundColor: ['#4CAF50', '#FFC107'], // Colors for each section
                        hoverBackgroundColor: ['#45A049', '#FFCA28'],
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                const value = tooltipItem.raw;
                                const total = data.total_projects;
                                const percentage = ((value / total) * 100).toFixed(2);
                                return `${tooltipItem.label}: ${value} (${percentage}%)`;
                            },
                        },
                    },
                },
            },
        });
    } catch (error) {
        console.error('Error fetching graph data:', error);
    }
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', fetchGraphDataAndRenderChart);


// Add click event listener to toggle 'active' class for feedback items
document.addEventListener('DOMContentLoaded', function () {
    const feedbackList = document.getElementById('feedback-list');

    feedbackList.addEventListener('click', function (event) {
        const clickedItem = event.target.closest('.feedback-item');

        if (clickedItem) {
            // Remove 'active' class from all feedback items
            document.querySelectorAll('.feedback-item').forEach(item => {
                item.classList.remove('active');
            });

            // Add 'active' class to the clicked item
            clickedItem.classList.add('active');
        }
    });
});
