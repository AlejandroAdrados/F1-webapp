const urlParams = new URLSearchParams(window.location.search);
const year = urlParams.get('year');
const race = urlParams.get('race');

$(document).ready(function () {
  const infoContainer = document.getElementById('yearRaceInfo');
  if (race !== null && year !== null) {
    infoContainer.innerText = `Temporada ${year} - Jornada ${race}`;
  }
});

function updateYearToOptions() {
  const yearFrom = parseInt(document.getElementById('yearFrom').value);
  const yearToSelect = document.getElementById('yearTo');

  yearToSelect.innerHTML = ''; // Limpiar opciones anteriores

  if (yearFrom === 'Selecciona un año' || yearFrom === '') {
    yearToSelect.innerHTML = '<option value="">Selecciona una opción</option>';
  }
  else {
    for (let year = yearFrom; year <= 2024; year++) {
      yearToSelect.innerHTML += `<option value="${year}">${year}</option>`;
    }
  }
}

function importFromInternet() {
  updateYearToOptions();
  $('.modal-body .row').show();
  $('#internetOption').show();
  document.getElementById('internetOption').onclick = getResultsFromInternet;
  $('#fileOption').hide();
  $('#fileInput').hide();
}

function showModal() {
  $("#yearFrom").val("");
  $('#databaseModal').modal('show');
  $('.modal-body .row').hide();
  $('#internetOption').show();
  document.getElementById('internetOption').onclick = importFromInternet;
  $('#fileOption').show();
}


function getResultsFromFile() {
  $('#fileInput').click();
  $('#fileInput').change(function () {
    const file = $(this).prop('files')[0];
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      $.ajax({
        url: '/api/results/file',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(response) {
          alert("Temporadas " + response + " importadas correctamente.");
        },
        error: function(xhr, status, error) {
          alert('Error al cargar el archivo: ' + error);
        }
      });
    }
  });
}


async function getResultsFromInternet() {
  // Ocultar los botones y el texto del modal, y mostrar la barra de progreso
  $('#internetOption, #importarArchivo, #yearFrom, #yearTo, #labelYearFrom, #labelYearTo').hide();
  $('.modal-body p').hide();
  $('.progress').show();
  const yearStart = parseInt(document.getElementById('yearFrom').value);
  const yearEnd = parseInt(document.getElementById('yearTo').value);
  const totalYears = yearEnd - yearStart + 1;
  let processedYears = 0;
  for (let year = yearStart; year <= yearEnd; year++) {
    const data = { year: year };
    $('#modal-text').show();
    document.getElementById('modal-text').innerText = 'Importando temporada ' + year + '...';
    try {
      const response = await fetch('/api/results/internet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error('Error en la respuesta de la API');
      }
      processedYears++;
      const progressPercentage = Math.round((processedYears / totalYears) * 100);
      updateProgressBar(progressPercentage);
      if (processedYears === totalYears) {
        alert('Resultados correctamente importados desde Internet');
        $('#modal-text').hide();
        window.location.reload();
      }
    } catch (error) {
      alert('Error al procesar el año ' + year + ' : ' + error);
      $('#apiOption, #importarArchivo').show();
      $('.modal-body p').show();
      $('.progress').hide();
      break;
    }
  }
}

function updateProgressBar(percentage) {
  const progressBar = document.getElementById('progressBar');
  progressBar.style.width = percentage + '%';
  progressBar.setAttribute('aria-valuenow', percentage);
}
