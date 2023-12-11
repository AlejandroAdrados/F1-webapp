// Lógica clasificación
$(document).ready(function () {
    $('#clasificationLink').click(function (e) {
        e.preventDefault();
        const yearSelector = $('#yearSelector');
        loadYearsForSelector(yearSelector);
        $('#yearModal').modal('show');
    });

    $('#yearSelectionForm').submit(function (e) {
        e.preventDefault();
        const race = $('#racesSelector').val();
        const year = $('#yearSelector').val();
        window.location.href = `/clasification?year=${year}&race=${race}`;
    });
});
$('#yearSelector').change(function() {
    var selectedYear = $(this).val();
    const yearSelector = $('#racesSelector');
    loadRacesForSelector(selectedYear, yearSelector);
});

// Lógica información de un piloto
$(document).ready(function() {
    $('#competitorLink').click(function (e) {
        e.preventDefault();
        const driverSelector = $('#yearSelectorDriver')
        loadYearsForSelector(driverSelector);
        $('#competitorModal').modal('show');
    });

    $('#driverSelectionForm').submit(function (e) {
        e.preventDefault();
        const driver = $('#driverSelector').val();
        const race = $('#racesSelectorDriver').val();
        const year = $('#yearSelectorDriver').val();
        window.location.href = `/competitor?year=${year}&race=${race}&driver=${driver}`;
    });
});
$('#yearSelectorDriver').change(function() {
    var selectedYear = $(this).val();
    const raceSelector = $('#racesSelectorDriver');
    loadRacesForSelector(selectedYear, raceSelector);
    loadDriversForSelector(selectedYear);
});

// Lógica para el cambio de icono en los elementos colapsables
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

// Funciones para rellenar selectores
function loadYearsForSelector(selector) {
    $.get('/api/years', function(data) {
        var years = data.map(function(item) {
            return item.year;
        });
        var defaultYear = years[0]
        for (var i = 0; i < years.length; i++) {
            selector.append($('<option>', {
                value: years[i],
                text: years[i]
            }));
        }
        selector.val(defaultYear).trigger('change');
    });
}

function loadRacesForSelector(selectedYear, selector) {
    $.get(`/api/races?year=${selectedYear}`, function(data) {
        var races = data.races;
        selector.empty();
        for (var i = 1; i <= races; i++) {
            selector.append($('<option>', {
                value: i,
                text: i
            }));
        }
    });
}

function loadDriversForSelector(selectedYear) {
    $.get(`/api/competitors/list?year=${selectedYear}`, function(data) {
        $('#driverSelector').empty(); 
        data.forEach(function(driver) {
            $('#driverSelector').append($('<option>', {
                value: driver,
                text: driver
            }));
        });
    });
}
