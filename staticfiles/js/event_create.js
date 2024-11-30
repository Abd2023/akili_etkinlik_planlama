document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('eventCreateForm');
    const inputs = form.querySelectorAll('input, select, textarea');
    const submitButton = form.querySelector('.submit-button');

    // Add live validation for inputs
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            if (input.checkValidity()) {
                input.style.borderColor = '#4caf50';
            } else {
                input.style.borderColor = '#ff5722';
            }
        });
    });

    // Add submit animation
    form.addEventListener('submit', (event) => {
        submitButton.textContent = 'Creating...';
        submitButton.disabled = true;

        setTimeout(() => {
            submitButton.textContent = 'Create Event';
            submitButton.disabled = false;
        }, 2000);
    });
});
