// Lógica para el cambio de icono en los elementos colapsables
document.addEventListener('DOMContentLoaded', function () {
    const collapseElements = document.querySelectorAll('.collapse-element');
    collapseElements.forEach(function (element) {
        element.addEventListener('click', function () {
            const icon = this.querySelector('span i');
            if (icon.classList.contains('bi-chevron-down')) {
                icon.classList.replace('bi-chevron-down', 'bi-chevron-up');
            } else {
                icon.classList.replace('bi-chevron-up', 'bi-chevron-down');
            }
        });
    });
});

// Lógica para mostrar/ocultar menú plots
$(document).ready(function() {
    const url = window.location.href;
    if (!url.includes('/metrics/plots')) {
        document.getElementById('plotManagement').style.display = 'none';
    }
});

// Lógica para mostrar/ocultar menú grafos
$(document).ready(function() {
    const url = window.location.href;
    if (!url.includes('/graph')) {
        document.getElementById('graphManagement').style.display = 'none';
    }
});
