
console.log('Si ta jalando bro 😏')

document.getElementById('login-button').addEventListener('click', async () => {
    // Obtener datos del formulario
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Validar campos vacíos
    if (!email || !password) {
        document.getElementById('respuesta').textContent = 'Por favor, llena todos los campos.';
        return;
    }

    try {
        // Enviar datos al backend
        const response = await fetch('http://10.3.13.71:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        // Procesar la respuesta
        if (response.ok) {
            const data = await response.json();
            if (data.exito) {
                document.getElementById('respuesta').textContent = 'Inicio de sesión exitoso.';
                window.location.href = 'dashboard';
                // window.location.href = 'dashboard.html';
            } else {
                document.getElementById('respuesta').textContent = data.mensaje || 'Credenciales incorrectas.';
                window.location.href = '/';
            }
        } else {
            document.getElementById('respuesta').textContent = 'Error en el servidor.';
        }
    } catch (error) {
        document.getElementById('respuesta').textContent = 'Error de conexión: ' + error.message;
    }
});
