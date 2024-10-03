
function redirectToLogout() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    window.location.href = `/housewise/logout/`;
}

function redirectToUser() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    window.location.href = `/housewise/${username}/menu/user/`;
}

function redirectToMaterials() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    window.location.href = `/housewise/${username}/menu/materials/`;
}

function redirectToFeedbacks() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    window.location.href = `/housewise/${username}/menu/feedbacks/`;
}

function redirectToScripts() {
    const username = document.querySelector('.dropdown-btn').dataset.username;
    window.location.href = `/housewise/${username}/scripts/`;
}
