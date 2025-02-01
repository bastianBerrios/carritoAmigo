const prevMonthButton = document.getElementById('prev-month');
const nextMonthButton = document.getElementById('next-month');
const monthYearLabel = document.getElementById('month-year');
const daysContainer = document.getElementById('days-container');

const eventModal = document.getElementById('event-modal');
const closeModalButton = document.getElementById('close-modal');
const saveEventButton = document.getElementById('save-event');
const cancelEventButton = document.getElementById('cancel-event');
const editEventButton = document.getElementById('edit-event'); // Botón para habilitar la edición

let currentDate = new Date();
let selectedDay = null;
let events = {}; // Para almacenar los eventos por día
let isNewEvent = false; // Variable que indica si estamos creando un evento nuevo

// Función para renderizar el calendario
function renderCalendar() {
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();
    const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    monthYearLabel.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const startingDay = firstDay.getDay();

    daysContainer.innerHTML = ''; // Limpiar los días previos

    // Generar los días vacíos antes del primer día del mes
    for (let i = 0; i < startingDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.classList.add('day-cell', 'other-month');
        daysContainer.appendChild(emptyCell);
    }

    // Crear los días del mes
    for (let day = 1; day <= totalDays; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('day-cell');
        
        // Si ya existe un evento para este día, lo muestra
        if (events[day]) {
            const { startTime, endTime } = events[day];
            dayCell.textContent = `${startTime} a ${endTime}`; // Mostrar la hora en lugar del número de día
            dayCell.style.backgroundColor = '#E68A6A';
            dayCell.style.color = 'white';
        } else {
            dayCell.textContent = day; // Mostrar el número del día solo si no hay evento
        }

        dayCell.onclick = () => openModal(day); // Al hacer clic se abre el modal
        daysContainer.appendChild(dayCell);
    }
}

// Función para abrir el modal y mostrar los datos del evento
function openModal(day) {
    selectedDay = day;
    const event = events[day] || {}; // Si no existe un evento, crea uno vacío

    // Rellenamos el formulario con los datos del evento
    document.getElementById('seller-name').value = event.sellerName || '';
    document.getElementById('seller-rut').value = event.sellerRut || '';
    document.getElementById('start-time').value = event.startTime || '';
    document.getElementById('end-time').value = event.endTime || '';
    document.getElementById('event-id').value = event.id || ''; // Para editar, usamos el ID del evento

    // Establecer si estamos creando un nuevo evento
    isNewEvent = !event.id;

    if (isNewEvent) {
        // Si es un nuevo evento, habilitamos los campos para edición
        enableFields();
    } else {
        // Si estamos editando un evento existente, deshabilitamos los campos
        disableFields();
    }

    eventModal.style.display = 'flex'; // Mostrar el modal
}

// Habilitar los campos para poder ser editados
function enableFields() {
    const inputs = document.querySelectorAll('.modal input');
    inputs.forEach(input => input.disabled = false); // Habilitar campos
}

// Deshabilitar los campos después de guardar el evento
function disableFields() {
    const inputs = document.querySelectorAll('.modal input');
    inputs.forEach(input => input.disabled = true); // Deshabilitar campos
}

// Limpiar los mensajes de error antes de realizar una nueva validación
function clearErrorMessages() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(msg => msg.remove()); // Eliminar mensajes de error previos

    const inputs = document.querySelectorAll('.input-error');
    inputs.forEach(input => input.classList.remove('input-error')); // Eliminar clase de error de los campos
}

// Validación del formulario antes de guardar el evento
function validateForm() {
    clearErrorMessages(); // Limpiar mensajes de error previos
    let valid = true;

    const sellerName = document.getElementById('seller-name').value;
    const sellerRut = document.getElementById('seller-rut').value;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;

    // Validación del nombre (no debe contener números)
    const nameRegex = /^[A-Za-zÁáÉéÍíÓóÚúÑñ ]+$/;
    if (!nameRegex.test(sellerName)) {
        const sellerNameInput = document.getElementById('seller-name');
        sellerNameInput.classList.add('input-error'); // Añadir borde rojo al campo
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = "El nombre no puede contener números.";
        sellerNameInput.parentElement.appendChild(errorMessage); // Añadir el mensaje debajo del campo
        valid = false;
    }

    // Verificar que todos los campos están completos
    if (!sellerName) {
        const sellerNameInput = document.getElementById('seller-name');
        sellerNameInput.classList.add('input-error'); // Añadir borde rojo al campo
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = "Este campo es obligatorio.";
        sellerNameInput.parentElement.appendChild(errorMessage); // Añadir el mensaje debajo del campo
        valid = false;
    }

    if (!sellerRut) {
        const sellerRutInput = document.getElementById('seller-rut');
        sellerRutInput.classList.add('input-error'); // Añadir borde rojo al campo
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = "Este campo es obligatorio.";
        sellerRutInput.parentElement.appendChild(errorMessage); // Añadir el mensaje debajo del campo
        valid = false;
    }

    if (!startTime) {
        const startTimeInput = document.getElementById('start-time');
        startTimeInput.classList.add('input-error'); // Añadir borde rojo al campo
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = "Este campo es obligatorio.";
        startTimeInput.parentElement.appendChild(errorMessage); // Añadir el mensaje debajo del campo
        valid = false;
    }

    if (!endTime) {
        const endTimeInput = document.getElementById('end-time');
        endTimeInput.classList.add('input-error'); // Añadir borde rojo al campo
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = "Este campo es obligatorio.";
        endTimeInput.parentElement.appendChild(errorMessage); // Añadir el mensaje debajo del campo
        valid = false;
    }

    return valid;
}

// Función para guardar o actualizar el evento
saveEventButton.onclick = () => {
    if (!validateForm()) {
        return; // Si la validación falla, no guardamos nada
    }

    const sellerName = document.getElementById('seller-name').value;
    const sellerRut = document.getElementById('seller-rut').value;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;
    const eventId = document.getElementById('event-id').value;

    const eventInfo = { sellerName, sellerRut, startTime, endTime };

    if (isNewEvent) {
        // Si estamos creando un nuevo evento
        const newEventId = Date.now(); // Usamos un timestamp como ID único
        events[selectedDay] = { ...eventInfo, id: newEventId };
    } else {
        // Si estamos editando un evento
        events[selectedDay] = { ...eventInfo, id: eventId };
    }

    renderCalendar(); // Volver a renderizar el calendario
    eventModal.style.display = 'none'; // Cerrar el modal

    // Bloquear los campos después de guardar
    disableFields();
};

// Función para cancelar la edición del evento
cancelEventButton.onclick = () => {
    eventModal.style.display = 'none'; // Cerrar el modal sin guardar cambios
};

// Función para cerrar el modal
closeModalButton.onclick = () => {
    eventModal.style.display = 'none'; // Cerrar el modal
};

// Función para navegar al mes anterior
prevMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

// Función para navegar al siguiente mes
nextMonthButton.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Función para habilitar la edición del evento
editEventButton.onclick = () => {
    enableFields(); // Habilitar campos para edición
};

// Inicializar el calendario
renderCalendar();
