$(document).ready(function() {
    let graphData = [];

    function loadNewGraph(year, race, isBonus) {
        $('#loading-spinner').show();
        let url = `/api/bgraph?year=${year}&race=${race}`;
        if (!isBonus) {
            url = `/api/graph?year=${year}&race=${race}`;
    }
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#loading-spinner').hide();
                const graphDiv = $('<div>').addClass('graph').appendTo('#graph');
                const graphId = `graph_${graphData.length + 1}`;
                $('<h3>').text(`Grafo temporada ${year} jornada ${race}`).appendTo(graphDiv);
                $('<div>').attr('id', graphId).appendTo(graphDiv);
                Plotly.newPlot(graphId, data);
                graphData.push(data);
    
                if (graphData.length >= 1) {
                    $('#loadAnotherGraphBtn').show();
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching graph data:', error);
                $('#loading-spinner').hide();
                $('#graph').text('Error loading graph data');
            }
        });
    }

    $('#loadAnotherGraphBtn').click(function(e) {
        e.preventDefault();
        const yearSel = $('#yearSelectorModal');
        loadYearsForSelector(yearSel);
        $('#graphModal').modal('show');
    });

    $('#yearSelectorModal').change(function() {
        var selectedYear = $(this).val();
        const raceSel = $('#racesSelectorModal');
        loadRacesForSelector(selectedYear, raceSel);
    });

    $('#graphSelectionForm').submit(function(e) {
        e.preventDefault();
        const race = $('#racesSelectorModal').val();
        const year = $('#yearSelectorModal').val();
        const isBonus = $('#bonificationCheckbox').is(':checked');
        $('#graphModal').modal('hide');
        loadNewGraph(year, race, isBonus);
    });

    document.getElementById("loadAnotherGraphBtn").click();
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