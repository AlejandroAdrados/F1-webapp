$(document).ready(function () {
    // Cuando se haga clic en "Clasificación"
    $('#clasificationLink').click(function (e) {
        e.preventDefault(); // Evitar que se ejecute el href del enlace
        $('#seleccionModal').modal('show'); // Mostrar el modal de selección
    });

    // Manejar el envío del formulario de selección
    $('#seleccionForm').submit(function (e) {
        e.preventDefault(); // Evitar la acción por defecto del formulario
        const jornada = $('#racesSelector').val();
        const anio = $('#yearSelector').val();
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

$(document).ready(function() {
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

