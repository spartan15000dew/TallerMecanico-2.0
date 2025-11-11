document.addEventListener('DOMContentLoaded', function() {
    const tipoUsuarioSelect = document.getElementById('tipo_usuario');
    const datosCliente = document.getElementById('datos_cliente');
    const datosMecanico = document.getElementById('datos_mecanico');

    function toggleFormularios() {
        if (tipoUsuarioSelect.value === 'Cliente') {
            datosCliente.style.display = 'block';
            datosMecanico.style.display = 'none';
        } else if (tipoUsuarioSelect.value === 'Mecanico') {
            datosCliente.style.display = 'none';
            datosMecanico.style.display = 'block';
        }
    }

    // Ejecutar al cargar la página
    toggleFormularios();

    // Ejecutar al cambiar la selección
    tipoUsuarioSelect.addEventListener('change', toggleFormularios);
});