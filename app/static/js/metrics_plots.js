$(document).ready(function() {
    let graphsArray = [];
    function loadNewPlot(year, race, isBonus) {
        $('#loading-spinner').show();
        $('#loadAnotherGraphMetricsBtn').hide();
        let url = `/api/metrics/bseason?year=${year}&race=${race}`;
        if (!isBonus) {
            url = `/api/metrics/season?year=${year}&race=${race}`;
        }
        $.get(url, function(data) {
            $('#loading-spinner').hide();
            $('#loadAnotherGraphMetricsBtn').show();
            graphsArray.push([year, race, isBonus])
            refreshList();
            const datos = data; // Datos obtenidos de la API
            const jornadas = datos.map(item => item[2]);
    
            // Preparar los datos para los gráficos por métrica
            const metricas = {
                'Grado Normalizado': [],
                'Peso Normalizado': [],
                'Coeficiente de Clustering': [],
                'Kendall': [],
                'Kendall Evolutivo': []
            };
    
            // Recorrer datos y añadir valores por métrica
            datos.forEach(item => {
                metricas['Grado Normalizado'].push(item[0]['Grado Normalizado']);
                metricas['Peso Normalizado'].push(item[0]['Peso Normalizado']);
                metricas['Coeficiente de Clustering'].push(item[0]['Coeficiente de Clustering']);
                metricas['Kendall'].push(item[0]['Kendall']);
                metricas['Kendall Evolutivo'].push(item[0]['Kendall Evolutivo']);
            });
    
            // Crear o actualizar gráficos por cada métrica
            Object.keys(metricas).forEach(metrica => {
                const divId = metrica.toLowerCase().replace(/ /g, '_');
                const existingPlot = document.getElementById(divId);
    
                const data = [
                    {
                        x: jornadas,
                        y: metricas[metrica],
                        type: 'scatter',
                        mode: 'lines',
                        name: `Temporada ${year} Jornada ${race}`
                    }
                ];
    
                if (existingPlot) {
                    Plotly.addTraces(divId, data);
                } else {
                    const div = document.createElement('div');
                    div.id = divId;
                    $('#graficos').append(div);
    
                    const layout = {
                        title: `Gráfica de evolución ${metrica}`,
                        xaxis: {
                            title: 'Jornada'
                        },
                        yaxis: {
                            title: `Valor de ${metrica}`
                        }
                    };
    
                    Plotly.newPlot(div.id, data, layout);
                }
            });
        });
    }
    
    function refreshList() {
        const graphList = document.getElementById('graphList');
        graphList.innerHTML = ''; // Vacía el contenido antes de cargar los nuevos elementos

        graphsArray.forEach(element => {
            const [year, race, isBonus] = element;
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');

            // Crear el contenido con la cruz
            const content = document.createElement('span');
            content.innerText = `Temporada ${year} Jornada ${race} ${isBonus ? 'bonificado' : 'no bonificado'}`;

            // Crear el botón de eliminar (cruz)
            const deleteButton = document.createElement('span');
            deleteButton.classList.add('delete-button');
            deleteButton.innerHTML = '&#10006;'; // Esto es el carácter unicode para la cruz
            deleteButton.href = '#';
            deleteButton.onclick = function() {
                // Lógica para eliminar este elemento específico
                listItem.remove();
            };

            // Añadir el contenido y la cruz al elemento li
            listItem.appendChild(content);
            listItem.appendChild(deleteButton);

            graphList.appendChild(listItem);
        });
    }
    
    $('#loadAnotherGraphMetricsBtn').click(function(e) {
            e.preventDefault();
            const yearSel = $('#yearSelectorPlotsModal');
            loadYearsForSelector(yearSel);
            $('#metricsModalPlots').modal('show');
    });
    
    $('#yearSelectorPlotsModal').change(function() {
        var selectedYear = $(this).val();
        const raceSel = $('#racesSelectorPlotsModal');
        loadRacesForSelector(selectedYear, raceSel);
    });

    $('#metricsPlotsSelectionForm').submit(function(e) {
        e.preventDefault();
        const race = $('#racesSelectorPlotsModal').val();
        const year = $('#yearSelectorPlotsModal').val();
        const isBonus = $('#bonificationCheckboxPlotsModal').is(':checked');
        $('#metricsModalPlots').modal('hide');
        loadNewPlot(year, race, isBonus);
    });

    document.getElementById("loadAnotherGraphMetricsBtn").click();
});
       
function loadYearsForSelector(selector) {
    $.get('/api/years', function(data) {
        selector.empty();
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
        selector.empty();
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
