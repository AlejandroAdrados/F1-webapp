$(document).ready(function() {
$('#actualizarDB').click(function() {
    $('#exampleModal').modal('show');
  });

  $('#apiOption').click(function() {
    // Ocultar los botones y el texto del modal, y mostrar el spinner
    $('#apiOption, #importarArchivo, #yearFrom, #yearTo, #labelYearFrom, #labelYearTo').hide();
    $('.modal-body p').hide();
    $('.spinner-border').show();
    const yearStart = parseInt(document.getElementById('yearFrom').value);
    const yearEnd = parseInt(document.getElementById('yearTo').value);
    
    const data = {
      year_start: yearStart,
      year_end: yearEnd
    };
    // Llamada a la API para "Resultados a Internet"
    fetch('/api/results', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (response.ok) {
        alert('Resultados correctamente importados desde Internet');
        window.location.reload();
      }
      // Mostrar de nuevo los botones y el texto después de la respuesta, y ocultar el spinner
      $('#apiOption, #importarArchivo').show();
      $('.modal-body p').show();
      $('.spinner-border').hide();
    })
    .catch(error => {
      console.error('Error al actualizar la base de datos:', error);
      // Mostrar de nuevo los botones y el texto en caso de error, y ocultar el spinner
      $('#apiOption, #importarArchivo').show();
      $('.modal-body p').show();
      $('.spinner-border').hide();
    });
  });

  $('#archivoOption').change(function() {
    const file = $(this).prop('files')[0];
    if (file) {
      // Implementar lógica para manejar el archivo seleccionado
      alert('Archivo seleccionado: ' + file.name);
    }
  });

  $('#importarArchivo').click(function() {
    $('#archivoOption').click();
  });
});

function updateYearToOptions() {
  const yearFrom = parseInt(document.getElementById('yearFrom').value);
  const yearToSelect = document.getElementById('yearTo');

  yearToSelect.innerHTML = ''; // Limpiar opciones anteriores

  for (let year = yearFrom; year <= 2023; year++) {
    yearToSelect.innerHTML += `<option value="${year}">${year}</option>`;
  }
}

// Obtener la jornada y el año de la URL (este es un ejemplo, ajusta la lógica según tu URL)
const urlParams = new URLSearchParams(window.location.search);
const year = urlParams.get('year');
const race = urlParams.get('race');


// Mostrar la información en el navbar
const infoContainer = document.getElementById('jornadaAnioInfo');
if (race !== null && year !== null) {
    infoContainer.innerText = `Temporada ${year} - Jornada ${race}`;
} else {
    infoContainer.innerText = 'Seleccione jornada y año';
}
