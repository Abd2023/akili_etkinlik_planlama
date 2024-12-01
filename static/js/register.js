
document.querySelectorAll('input, textarea, select').forEach(input => {
    input.addEventListener('focus', () => {
        input.style.borderColor = '#FF4B2B';
    });
    input.addEventListener('blur', () => {
        input.style.borderColor = '#ccc';
    });
});


const form = document.querySelector('form');

form.addEventListener('submit', async (event) => {
    event.preventDefault(); 

    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: form.method,
            body: formData,
        });

        if (response.ok) {
            alert("Registration Successful!");
            form.reset(); 
        } else {
            const errors = await response.json();
            alert("Registration Failed: " + JSON.stringify(errors));
        }
    } catch (error) {
        console.error("Error during registration:", error);
        alert("An error occurred. Please try again.");
    }
});
