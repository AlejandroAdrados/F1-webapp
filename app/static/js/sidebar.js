// Lógica cambio temporada/jornada
$(document).ready(function () {
    $('#clasificationLink').click(function (e) {
        window.location.href = `/clasificacion?year=${year}&race=${race}`;
    });
});

// Lógica cambio temporada/jornada
$(document).ready(function () {
    $('#changeLink').click(function (e) {
        e.preventDefault(); // Evitar que se ejecute el href del enlace
        $('#yearModal').modal('show'); // Mostrar el modal de selección
    });

    // Manejar el envío del formulario de selección
    $('#yearSelectionForm').submit(function (e) {
        e.preventDefault(); // Evitar la acción por defecto del formulario
        const race = $('#racesSelector').val();
        const year = $('#yearSelector').val();
        // Redirigir a la página de clasificación con los parámetros de jornada y año
        window.location.href = `/clasificacion?year=${year}&race=${race}`;
    });
    $.get('/api/years', function(data) {
        var years = data.map(function(item) {
            return item.year;
        });
        var defaultYear = years[0]
        for (var i = 0; i < years.length; i++) {
            $('#yearSelector').append($('<option>', {
                value: years[i],
                text: years[i]
            }));
        }
        $('#yearSelector').val(defaultYear).trigger('change');
    });
});

$('#yearSelector').change(function() {
    var selectedYear = $(this).val();
    $.get('/api/races?year=' + selectedYear, function(data) {
        var races = data.races;
        $('#racesSelector').empty(); // Limpiar las opciones anteriores
        for (var i = 1; i <= races; i++) {
            $('#racesSelector').append($('<option>', {
                value: i,
                text: i
            }));
        }
    });
});

// Lógica información de un piloto
$(document).ready(function() {
    // Hacer la petición GET a /api/competitors/list
    $.get(`/api/competitors/list?year=${year}`, function(data) {
        console.log(data);
        const driverSelector = $('#driverSelector');
        // Iterar sobre los datos y agregar opciones al select
        data.forEach(function(driver) {
            driverSelector.append($('<option></option>').text(driver.driver_name).val(driver.driver_name));
        });
    });
    $('#competitorLink').click(function (e) {
        e.preventDefault(); // Evitar que se ejecute el href del enlace
        $('#competitorModal').modal('show'); // Mostrar el modal de selección
    });

    $('#driverSelectionForm').submit(function (e) {
        e.preventDefault(); // Evitar la acción por defecto del formulario
        const driver = $('#driverSelector').val();
        // Redirigir a la página de clasificación con los parámetros de jornada y año
        window.location.href = `/competitor?year=${year}&race=${race}&driver=${driver}`;
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



