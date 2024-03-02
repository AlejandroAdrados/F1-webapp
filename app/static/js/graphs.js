let graphData = [];
let graphsArray = [];

function loadNewGraph(year, race, isBonus) {
    $("#loading-spinner").show();
    $("#loadAnotherGraph").hide();
    $.ajax({
        url: `/api/graph?year=${year}&race=${race}&bonus=${isBonus}`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#loading-spinner").hide();
            $("#loadAnotherGraph").show();
            graphsArray.push([year, race, isBonus]);
            refreshList();
            $("<h4>")
                .text(
                    `Grafo temporada ${year} jornada ${race} 
            ${isBonus ? "bonificado" : "no bonificado"}`
                )
                .appendTo("#graph");
            const graphDiv = $("<div>").addClass("graph").appendTo("#graph");
            const graphId = `graph_${graphData.length + 1}`;
            $("<div>").attr("id", graphId).appendTo(graphDiv);
            const config = { resposive: true };
            Plotly.newPlot(graphId, data, config);
            window.addEventListener("resize", function () {
                Plotly.relayout(graphId, {
                    width: graphDiv.width(),
                    height: graphDiv.height(),
                });
            });
            graphData.push(data);

            if (graphData.length >= 1) {
                $("#loadAnotherGraph").show();
            }
        },
        error: function () {
            $("#loading-spinner").hide();
            $("#graph").text("Error al cargar el grafo. Pruebe actualizando su base de datos.");
        },
    });
}

function refreshList() {
    const graphsList = document.getElementById("graphsList");
    graphsList.innerHTML = ""; // Vacía el contenido antes de cargar los nuevos elementos
    graphsArray.forEach((element) => {
        const [year, race, isBonus] = element;
        const listItem = document.createElement("li");
        listItem.classList.add("list-group-item");
        const content = document.createElement("span");
        content.innerText = `Temporada ${year} Jornada ${race} ${isBonus ? "bonificado" : "no bonificado"
            }`;
        const deleteButton = document.createElement("span");
        deleteButton.classList.add("delete-button");
        deleteButton.innerHTML = "&#10006;"; // Carácter unicode para la cruz
        deleteButton.href = "#";
        deleteButton.onclick = function () {
            const index = $(this).parent().index();
            deleteGraph(index);
            graphsArray.splice(index, 1);
            listItem.remove();
        };
        listItem.appendChild(content);
        listItem.appendChild(deleteButton);
        graphsList.appendChild(listItem);
    });
}

function deleteGraph(index) {
    const container = document.getElementById("graph");
    const elementsPerGraph = 2; //Título y grafo
    const startChildIndex = index * elementsPerGraph;

    if (container && container.childNodes.length > startChildIndex + 1) {
        for (let i = 0; i < elementsPerGraph; i++) {
            const element = container.childNodes[startChildIndex];
            container.removeChild(element);
        }
    }
}

//Modal functions
function loadYearsForSelector(selector) {
    $.get("/api/years", function (data) {
        selector.empty();
        var years = data.map(function (item) {
            return item.year;
        });
        var defaultYear = years[0];
        for (var i = 0; i < years.length; i++) {
            selector.append(
                $("<option>", {
                    value: years[i],
                    text: years[i],
                })
            );
        }
        selector.val(defaultYear).trigger("change");
    });
}

function loadRacesForSelector(selectedYear, selector) {
    $.get(`/api/races?year=${selectedYear}`, function (data) {
        selector.empty();
        var races = data.races;
        selector.empty();
        for (var i = 1; i <= races; i++) {
            selector.append(
                $("<option>", {
                    value: i,
                    text: i,
                })
            );
        }
    });
}

$(document).ready(function () {
    $("#loadAnotherGraph").click(function (e) {
        e.preventDefault();
        const yearSel = $("#yearSelectorModal");
        loadYearsForSelector(yearSel);
        $("#bonificationCheckbox").prop("checked", false);
        $("#graphModal").modal("show");
    });

    $("#yearSelectorModal").change(function () {
        var selectedYear = $(this).val();
        const raceSel = $("#racesSelectorModal");
        loadRacesForSelector(selectedYear, raceSel);
    });

    $("#graphSelectionForm").submit(function (e) {
        e.preventDefault();
        const race = $("#racesSelectorModal").val();
        const year = $("#yearSelectorModal").val();
        const isBonus = $("#bonificationCheckbox").is(":checked");
        $("#graphModal").modal("hide");
        loadNewGraph(year, race, isBonus);
    });

    document.getElementById("loadAnotherGraph").click();
});
