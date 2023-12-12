const isBonus = urlParams.get('bonus');
function getData() {
    let url = `/api/metrics/branking?year=${year}&race=${race}`;
    if (isBonus === 'false') {
        url = `/api/metrics/ranking?year=${year}&race=${race}`;
    }
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            $('#clustering-coefficient').append(data["Coeficiente de Clustering"]);
            $('#normalized-degree').append(data["Grado Normalizado"]);
            $('#kendall').append(data["Kendall"]);
            $('#evolutionary-kendall').append(data["Kendall Evolutivo"]);
            $('#normalized-weight').append(data["Peso Normalizado"]);
        },
        error: function(error) {
          console.error('Error fetching data:', error);
        }
    });
}

$(document).ready(function () {
    getData();
});
