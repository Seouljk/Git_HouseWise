// Function to redirect to the menu page
function redirectToMenu(username) {
    window.location.href = "/housewise/" + username + "/menu/";
}

// Function to update the countdown and status
function updateCountdownAndStatus() {
    const now = new Date();
    const midnight = new Date();
    
    // Set midnight to the next day
    midnight.setHours(24, 0, 0, 0);
    
    // Calculate the time remaining until midnight
    const remainingTime = midnight - now;
    
    // Get hours, minutes, and seconds
    const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
    
    // Update the countdown display
    document.getElementById('hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
}

// Update the status based on the toggle
function updateStatus() {
    const statusText = document.getElementById('status-text');
    const statusIndicator = document.getElementById('status-indicator');
    const statusToggle = document.getElementById('status-toggle');

    if (statusToggle.checked) {
        // If toggle is on
        statusText.textContent = 'Online';
        statusIndicator.textContent = '●';
        statusIndicator.classList.remove('offline');
        statusIndicator.classList.add('online');
    } else {
        // If toggle is off
        statusText.textContent = 'Offline';
        statusIndicator.textContent = '●';
        statusIndicator.classList.remove('online');
        statusIndicator.classList.add('offline');
    }
}

// Update status on toggle change
document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("status-toggle");
    const crawlerStatusMessage = document.getElementById("crawler-status-message");

    // Function to update crawler status message
    function updateCrawlerStatus() {
        if (toggle.checked) {
            crawlerStatusMessage.textContent = "Crawler is on";
            crawlerStatusMessage.style.color = "green"; // Change text color to green
        } else {
            crawlerStatusMessage.textContent = "Crawler is off";
            crawlerStatusMessage.style.color = "red"; // Change text color to red
        }
    }

    // Initial status setup
    updateCrawlerStatus();
    updateStatus(); // Ensure initial status text and indicator are set

    // Event listener for toggle change
    toggle.addEventListener("change", function() {
        updateCrawlerStatus();
        updateStatus(); // Update status text and indicator based on toggle
    });




});

// Update the countdown every second
setInterval(function() {
    updateCountdownAndStatus();
    updateStatus(); // Update the status every second to reflect the toggle's state
}, 1000);


