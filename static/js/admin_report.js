document.addEventListener('DOMContentLoaded', () => {
    const statCards = document.querySelectorAll('.stat-card');
    const userListItems = document.querySelectorAll('.user-list li');

    
    statCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.transform = 'scale(1.1)';
        });
        card.addEventListener('mouseout', () => {
            card.style.transform = 'scale(1)';
        });
    });

   
    userListItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.backgroundColor = '#d9f0ff';
        });
        item.addEventListener('mouseout', () => {
            item.style.backgroundColor = '#f0f8ff';
        });
    });
});
