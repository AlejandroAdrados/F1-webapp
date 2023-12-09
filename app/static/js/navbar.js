$(document).ready(function() {
$('#actualizarDB').click(function() {
    $('#exampleModal').modal('show');
  });

  $('#apiOption').click(function() {
    // Ocultar los botones y el texto del modal, y mostrar el spinner
    $('#apiOption, #importarArchivo').hide();
    $('.modal-body p').hide();
    $('.spinner-border').show();

    // Llamada a la API para "Resultados a Internet"
    fetch('/api/results', {
      method: 'POST',
      // Puedes incluir headers o datos en la solicitud si es necesario
    })
    .then(response => {
      if (response.ok) {
        alert('Resultados correctamente importados desde Internet');
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