document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    togglePassword.addEventListener('click', function (e) {
        // Alterna el tipo de input entre password y text
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        
        // Alterna el texto del botón entre 'Mostrar' y 'Ocultar'
        this.textContent = this.textContent === 'Mostrar' ? 'Ocultar' : 'Mostrar';
    });
});

