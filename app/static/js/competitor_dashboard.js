const driver = urlParams.get('driver');
function updateDriver() {
    $('#driver').text(driver);
}
function getScore() {
    $.get(`/api/competitor/score?year=${year}&race=${race}&driver=${driver}`, function (data) {
        $('#score-text').text(data);
    });
}

function getPosition() {
    $.get(`/api/competitor/position?year=${year}&race=${race}&driver=${driver}`, function (data) {
        $('#position-text').text(data);
    });
}

function getHistory() {
    $.get(`/api/competitors/num?year=${year}`, function (numCompetitors) {
        $.get(`/api/competitor/history?year=${year}&race=${race}&driver=${driver}`, function (data) {
            const races = [];
            const positions = [];

            data.forEach(item => {
                races.push(item.race);
                positions.push(item.position);
            });

            const trace = {
                x: races,
                y: positions,
                type: 'scatter',
                mode: 'lines+markers',
                marker: {
                    color: 'black',
                    size: 10  // Tamaño de los puntos, puedes ajustarlo según lo necesites
                },
                line: {
                    shape: 'linear'  // Establecer líneas rectas en lugar de curvas
                }
            };

            const layout = {
                xaxis: { 
                    title: 'Jornada',
                    range: [0, races.length + 1]
                },
                yaxis: {
                    title: 'Posición',
                    autorange: 'reversed', // Invertir el eje y
                    tickvals: Array.from({ length: numCompetitors }, (_, i) => i + 1), // Valores del 1 al 22
                    tickmode: 'array', // Establecer el modo de marcado como array
                    rangemode: 'tozero' // Asegurarse de que el rango comience desde cero
                }
            };

            // Renderizar el gráfico utilizando Plotly
            Plotly.newPlot('history-chart', [trace], layout);
        });
    });
}

$(document).ready(function () {
    updateDriver();
    getScore();
    getPosition();
    getHistory();
});
