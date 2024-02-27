const isBonus = urlParams.get('bonus');
function setProgressLevel(metricId, value) {
        const progressBar = document.getElementById(`${metricId}-level`);
        const normalizedValue = Math.min(Math.max(value, 0), 1);
        progressBar.style.width = `${normalizedValue * 100}%`;
    }

function getData() {
    let url = `/api/metrics/branking?year=${year}&race=${race}`;
    if (isBonus === 'false') {
        url = `/api/metrics/ranking?year=${year}&race=${race}`;
    }
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            $('#clustering-coefficient').append(parseFloat(data["Coeficiente de Clustering"]).toFixed(6));
            $('#normalized-degree').append(parseFloat(data["Grado Normalizado"]).toFixed(6));
            $('#kendall').append(parseFloat(data["Kendall"]).toFixed(6));
            $('#evolutionary-kendall').append(parseFloat(data["Kendall Evolutivo"]).toFixed(6));
            $('#normalized-weight').append(parseFloat(data["Peso Normalizado"]).toFixed(6));
            setProgressLevel('normalized-degree', data['Grado Normalizado']);
            setProgressLevel('normalized-weight', data['Peso Normalizado']);
            setProgressLevel('clustering-coefficient', data['Coeficiente de Clustering']);
            setProgressLevel('kendall', data['Kendall']);
            setProgressLevel('evolutionary-kendall', data['Kendall Evolutivo']);
        },
        error: function(error) {
          console.error('Error fetching data:', error);
        }
    });
}

$(document).ready(function () {
    getData();
});

document.querySelectorAll('.info-icon').forEach(icon => {
    icon.addEventListener('click', () => {
        const infoContent = icon.parentElement.nextElementSibling;
        infoContent.classList.toggle('active');
    });
});
