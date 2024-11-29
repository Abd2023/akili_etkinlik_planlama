// Profile Animation
document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-button');
    const backButton = document.querySelector('.back-button');

    // Add animation on button hover
    [editButton, backButton].forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseout', () => {
            button.style.transform = 'scale(1)';
        });
    });
});
