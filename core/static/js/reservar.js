document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const nombreInput = document.getElementById('nombre');
    const correoInput = document.getElementById('correo');
    const telefonoInput = document.getElementById('telefono');
    const lugarInput = document.getElementById('lugar');
    const tamanoInput = document.getElementById('tamano');
    const horaInput = document.getElementById('hora');
    const descripcionInput = document.getElementById('descripcion');
    const erroresDiv = document.createElement('div');

    // Agrega un contenedor de errores debajo del formulario
    erroresDiv.id = 'errores';
    erroresDiv.classList.add('alert', 'alert-danger', 'mt-3', 'd-none');
    form.parentElement.appendChild(erroresDiv);

    // Función para obtener la hora de Santiago, Chile
    function obtenerHoraSantiago() {
        const url = 'https://app.abstractapi.com/api/v1/timezone/';
        const apiKey = '8f37568d3c394d64b171cbe6be25c9ab';
    
        // Realiza la solicitud a la API AbstractAPI
        fetch(`${url}?api_key=${apiKey}&location=Santiago`)
            .then(response => response.json())
            .then(data => {
                if (data && data.datetime) {
                    const horaSantiago = data.datetime;
                    // Muestra la hora en el elemento con id 'horaSantiago'
                    const horaElement = document.getElementById('horaSantiago');
                    horaElement.textContent = `Hora de Santiago, Chile: ${horaSantiago}`;
                    // Cambia el color del texto a naranja
                    horaElement.style.color = 'orange'; 
                } else {
                    console.error('No se pudo obtener la hora.');
                }
            })
            .catch(error => console.error('Error al realizar la solicitud:', error));
    }

    // Llamar a la función para obtener la hora de Santiago
    obtenerHoraSantiago();

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Evita el envío del formulario para validación
        erroresDiv.innerHTML = '';
        erroresDiv.classList.add('d-none'); // Oculta mensajes de error al inicio
        let errores = [];

        // Validaciones
        if (!validarNombre(nombreInput.value)) {
            errores.push('El nombre debe tener al menos 3 caracteres.');
        }
        if (!validarCorreo(correoInput.value)) {
            errores.push('El correo electrónico no es válido.');
        }
        if (!validarTelefono(telefonoInput.value)) {
            errores.push('El número de teléfono debe contener solo dígitos y tener al menos 9 caracteres.');
        }
        if (!validarCampoRequerido(lugarInput.value)) {
            errores.push('El lugar del tatuaje no puede estar vacío.');
        }
        if (!validarCampoRequerido(tamanoInput.value)) {
            errores.push('El tamaño aproximado no puede estar vacío.');
        }
        if (horaInput.value === '') {
            errores.push('Por favor selecciona una hora preferida.');
        }
        if (!validarCampoRequerido(descripcionInput.value)) {
            errores.push('La descripción del tatuaje no puede estar vacía.');
        }

        // Si hay errores, los muestra
        if (errores.length > 0) {
            erroresDiv.classList.remove('d-none');
            errores.forEach((error) => {
                const errorP = document.createElement('p');
                errorP.textContent = error;
                erroresDiv.appendChild(errorP);
            });
        } else {
            // Si no hay errores, envía el formulario (o realiza acciones)
            alert('Reserva enviada con éxito');
            form.reset();
        }
    });

    // Funciones de validación
    function validarNombre(nombre) {
        return nombre.trim().length >= 3;
    }

    function validarCorreo(correo) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(correo);
    }

    function validarTelefono(telefono) {
        const phoneRegex = /^[0-9]{9,}$/; // Al menos 9 dígitos
        return phoneRegex.test(telefono);
    }

    function validarCampoRequerido(campo) {
        return campo.trim() !== '';
    }
});
