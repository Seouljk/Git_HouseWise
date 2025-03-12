function redirectToMenu(event) {
    event.preventDefault(); // Prevent the form from submitting
    const username = "{{ user.username }}"; // Ensure this variable is correctly set
    console.log("Redirecting to menu for user:", username);
    window.location.href = `/housewise/${username}/menu/`; // Ensure trailing slash
}

function enableEditing(inputId) {
    const inputField = document.getElementById(inputId);
    inputField.disabled = false; // Allow editing

    // Get the input element and the parent div
    const inputElement = document.getElementById(inputId);
    const parentDiv = inputElement.closest('div'); // Get the parent div


    // Enable editing on the input field
    inputElement.disabled = false;

    // Highlight the parent div
    parentDiv.classList.add('highlight');

    // Enable the save button
    document.getElementById('save-btn').disabled = false;

    // Optionally, focus on the input field
    inputElement.focus();

    const saveButton = document.getElementById('save-btn');
    saveButton.classList.add('enabled'); // Add enabled class for CSS
    saveButton.disabled = false; // Remove disabled state

    // Listen for input changes to keep save button enabled
    inputField.addEventListener('input', function () {
        saveButton.disabled = false; // Keep button enabled when editing
    });
}

// Modify saveChanges function to remove highlight when saving
function saveChanges() {
    const nameField = document.getElementById('user-name').value;
    const usernameField = document.getElementById('user-username').value;
    const emailField = document.getElementById('user-email').value;
    const passwordField = document.getElementById('user-password').value; // Capture the password
    const ageField = document.getElementById('user-birthdate').value; // Corrected ID for age

    // Only include the password if it's not empty
    const payload = {
        'name': nameField,
        'username': usernameField,
        'email': emailField,
        'age': ageField
    };

    // Include the password only if it has been entered
    if (passwordField) {
        payload.password = passwordField;
    }

    // Send an AJAX request to save the changes
    fetch("{% url 'save_profile_changes' user.username %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Add CSRF token for security
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // After saving, disable the input and the save button
            const inputs = ['user-name', 'user-username', 'user-email', 'user-password', 'user-birthdate'];
            inputs.forEach(inputId => {
                const input = document.getElementById(inputId);
                input.disabled = true; // Disable the input
                input.classList.remove('highlight'); // Remove highlight class
            });
            const saveButton = document.getElementById('save-btn');
            saveButton.disabled = true; // Disable the save button
            saveButton.classList.remove('enabled'); // Remove enabled class for CSS
        } else {
            alert('Error saving changes');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('Error saving changes');
    });
}

