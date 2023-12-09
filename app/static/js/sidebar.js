$(document).ready(function () {
    // Cuando se haga clic en "Clasificación"
    $('#clasificationLink').click(function (e) {
        e.preventDefault(); // Evitar que se ejecute el href del enlace
        $('#seleccionModal').modal('show'); // Mostrar el modal de selección
    });

    // Manejar el envío del formulario de selección
    $('#seleccionForm').submit(function (e) {
        e.preventDefault(); // Evitar la acción por defecto del formulario
        const jornada = $('#jornada').val();
        const anio = $('#anio').val();
        // Redirigir a la página de clasificación con los parámetros de jornada y año
        window.location.href = `/clasificacion?jornada=${jornada}&anio=${anio}`;
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const collapseElements = document.querySelectorAll('.collapse-element');
    collapseElements.forEach(function (element) {
        element.addEventListener('click', function () {
            const icon = this.querySelector('span i');
            if (icon.classList.contains('bi-chevron-down')) {
                icon.classList.replace('bi-chevron-down', 'bi-chevron-up');
            } else {
                icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
            }
        });
    });
});

// Obtener referencias a los elementos select
const selectAnio = document.getElementById('anio');
const selectJornada = document.getElementById('jornada');

// Realizar una solicitud GET a la API para obtener los datos
function obtenerDatos() {
    fetch('/api/info')
        .then(response => response.json())
        .then(data => {
            llenarDesplegables(data); // Llamar a la función para llenar los desplegables con los datos obtenidos
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Función para llenar dinámicamente las opciones del select de años y jornadas
function llenarDesplegables(data) {
    data.forEach(function(item) {
        const optionAnio = document.createElement('option');
        optionAnio.value = item.year;
        optionAnio.textContent = item.year;
        selectAnio.appendChild(optionAnio);
    });

    // Evento al seleccionar un año
    selectAnio.addEventListener('change', function() {
        const selectedYear = parseInt(this.value); // Obtener el año seleccionado como entero

        // Vaciar el desplegable de jornadas
        selectJornada.innerHTML = "";

        if (!isNaN(selectedYear)) {
            // Obtener el objeto correspondiente al año seleccionado
            const yearData = data.find(item => item.year === selectedYear);

            if (yearData) {
                // Hacer un bucle del 1 al número de carreras (num_races) correspondiente a ese año
                for (let i = 1; i <= yearData.num_races; i++) {
                    const optionJornada = document.createElement('option');
                    optionJornada.value = i;
                    optionJornada.textContent = `Jornada ${i}`;
                    selectJornada.appendChild(optionJornada);
                }
            } else {
                const optionJornada = document.createElement('option');
                optionJornada.textContent = "Selecciona un año primero";
                selectJornada.appendChild(optionJornada);
            }
        }
    });
}

// Obtener datos cuando la página se carga
obtenerDatos();

