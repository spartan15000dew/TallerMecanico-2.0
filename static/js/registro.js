// Espera a que todo el HTML esté cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function() {

    const tipoSelect = document.getElementById('tipo_usuario');
    const datosCliente = document.getElementById('datos_cliente');
    const datosMecanico = document.getElementById('datos_mecanico');

    function mostrarCampos() {
        // Asegúrate de que los elementos existen antes de usarlos
        if (!tipoSelect || !datosCliente || !datosMecanico) {
            return;
        }
        
        const tipo = tipoSelect.value;
        if (tipo === 'Cliente') {
            datosCliente.style.display = 'block';
            datosMecanico.style.display = 'none';
        } else if (tipo === 'Mecanico') {
            datosCliente.style.display = 'none';
            datosMecanico.style.display = 'block';
        }
    }

    // Añade el "listener" solo si el dropdown existe en la página
    if (tipoSelect) {
        tipoSelect.addEventListener('change', mostrarCampos);
    }

});