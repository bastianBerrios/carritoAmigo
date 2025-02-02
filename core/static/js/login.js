document.addEventListener('DOMContentLoaded', function () {  
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    form.addEventListener('submit', function (e) {
        // Esta línea evita que se envíe el formulario automáticamente
        e.preventDefault();
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        const erroresDiv = document.getElementById('errores') || crearDivErrores();

        // Limpia mensaje de errores
        erroresDiv.innerHTML = '';

        // Valida email
        if (!validarEmail(email)) {
            mostrarError(erroresDiv, 'Por favor ingresa un correo electrónico válido.');
            emailInput.focus();
            return;
        }

        // Valida contraseña
        const passwordErrors = validarPassword(password);
        if (passwordErrors.length > 0) {
            passwordErrors.forEach((error) => mostrarError(erroresDiv, error));
            passwordInput.focus();
            return;
        }

        // Validar credenciales contra los usuarios temporales
        const usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
        const usuarioValido = usuarios.find(
            (usuario) => usuario.email === email && usuario.password === password
        );

        if (!usuarioValido) {
            mostrarError(erroresDiv, 'Credenciales incorrectas. Intenta nuevamente.');
            return;
        }

        // Si las credenciales son correctas
        alert('Inicio de sesión exitoso');
        // Redirigir a "job.html"
        window.location.href = "job.html";
    });

    function crearDivErrores() {
        const erroresDiv = document.createElement('div');
        erroresDiv.id = 'errores';
        erroresDiv.classList.add('alert', 'alert-danger', 'mt-3');
    
        // Inserta el contenedor de errores después del botón de envío
        const botonSubmit = form.querySelector('button[type="submit"]');
        botonSubmit.parentElement.insertBefore(erroresDiv, botonSubmit.nextSibling);
    
        return erroresDiv;
    }
    

    /**
     * Muestra un mensaje de error en el contenedor de errores
     * @param {HTMLElement} contenedor - Contenedor donde se mostrarán los errores
     * @param {string} mensaje - Mensaje de error a mostrar
     */
    function mostrarError(contenedor, mensaje) {
        const errorItem = document.createElement('p');
        errorItem.textContent = mensaje;
        contenedor.appendChild(errorItem);
    }

    /**
     * Valida si el email tiene un formato válido
     * @param {string} email
     * @returns {boolean}
     */
    function validarEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Valida si la contraseña cumple con los criterios
     * @param {string} password - Contraseña ingresada
     * @returns {string[]} - Lista de errores encontrados
     */
    function validarPassword(password) {
        const errores = [];
        if (password.length < 6) {
            errores.push('La contraseña debe tener al menos 6 caracteres.');
        }
        return errores;
    }
});

// Usuarios temporales para el login
const usuariosTemporales = [
    { email: "xbastianberrios@gmail.com", password: "pass123" },
    { email: "fernandoalmonacid@gmail.com", password: "contra456" }
];

// Guardar usuarios en LocalStorage (solo si no están guardados ya)
if (!localStorage.getItem("usuarios")) {
    localStorage.setItem("usuarios", JSON.stringify(usuariosTemporales));
}