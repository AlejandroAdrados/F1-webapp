const driver = urlParams.get("driver");

function getInfo() {
  $("#driver-text").text(driver);
  $.ajax({
    url: `/api/competitor/info?year=${year}&race=${race}&driver=${driver}`,
    method: "GET",
    success: function (data) {
      $("#score-text").text(data["score"]);
      $("#position-text").text(data["position"] + "º");
      $("#team-text").text(data["team"]);
    },
    error: function () {
      window.location.href = "/error";
    },
  });
}

function getHistory() {
  $.get(
    `/api/competitor/history?year=${year}&race=${race}&driver=${driver}`,
    function (data) {
      const races = [];
      const positions = [];
      data.forEach((item) => {
        races.push(item.race);
        positions.push(item.position);
      });
      const trace = {
        x: races,
        y: positions,
        type: "scatter",
        mode: "lines+markers",
        marker: {
          color: "black",
          size: 10,
        },
        line: {
          shape: "linear",
        },
      };
      const layout = {
        title: `Historial de posiciones de ${driver} en la temporada ${year}`,
        xaxis: {
          title: "Jornada",
          range: [0.8, races.length + 0.2],
          tickformat: ",d",
          fixedrange: true,
        },
        yaxis: {
          title: "Posición",
          autorange: "reversed",
          tickformat: ",d",
          fixedrange: true,
        },
      };
      Plotly.newPlot("history-chart", [trace], layout);
    }
  );
}

$(document).ready(function () {
  getInfo();
  getHistory();
});
