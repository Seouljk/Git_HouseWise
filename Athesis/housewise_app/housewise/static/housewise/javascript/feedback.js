function redirectToMenu() {
    const username = "{{ user.username }}"; // Ensure this variable is correctly set
    console.log("Redirecting to menu for user:", username);
    window.location.href = `/housewise/${username}/menu/`; // Ensure trailing slash
}


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
        const response = await fetch('/housewise/api/feedbacks/'); // Absolute path
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
            document.getElementById('feedback-username').textContent = feedback.user;

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


