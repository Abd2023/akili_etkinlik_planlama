document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.querySelector('.save-btn');

    saveButton.addEventListener('click', () => {
        alert('Saving changes...');
    });

    saveButton.addEventListener('mouseover', () => {
        saveButton.style.transform = 'scale(1.1)';
    });

    saveButton.addEventListener('mouseout', () => {
        saveButton.style.transform = 'scale(1)';
    });
});
