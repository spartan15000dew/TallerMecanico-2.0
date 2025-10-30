
const citas = [
  {
    placa: "TRK-9821",
    marca: "Freightliner",
    modelo: "Cascadia",
    ano: 2019,
    propietario: "Transportes del Norte S.A.",
    fecha: "10/09/2025 08:00",
    motivo: "Revisión sistema de frenos de aire",
    estado: "Pendiente",
    costo: "$450.000"
  },
  {
    placa: "CLH-4420",
    marca: "Volvo",
    modelo: "FH16",
    ano: 2021,
    propietario: "Logística Sur Ltda.",
    fecha: "12/09/2025 11:30",
    motivo: "Cambio de embrague",
    estado: "En proceso",
    costo: "$1.200.000"
  },
  {
    placa: "SCN-7745",
    marca: "Scania",
    modelo: "R500",
    ano: 2018,
    propietario: "Camiones Express",
    fecha: "14/09/2025 14:00",
    motivo: "Reparación caja de cambios",
    estado: "Pendiente",
    costo: "$2.800.000"
  },
  {
    placa: "MBX-3309",
    marca: "Mercedes-Benz",
    modelo: "Actros",
    ano: 2020,
    propietario: "Transporte Patagonia",
    fecha: "16/09/2025 09:30",
    motivo: "Mantenimiento general + cambio de filtros",
    estado: "Finalizado",
    costo: "$650.000"
  }
];

function cargarCitas() {
  const tbody = document.getElementById("tabla-citas");
  tbody.innerHTML = "";

  citas.forEach((cita, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${cita.placa}</td>
      <td>${cita.marca} ${cita.modelo}</td>
      <td>${cita.ano}</td>
      <td>${cita.propietario}</td>
      <td>${cita.fecha}</td>
      <td>${cita.motivo}</td>
      <td>${cita.estado}</td>
      <td>${cita.costo}</td>
    `;
    tbody.appendChild(row);
  });
}

document.addEventListener("DOMContentLoaded", cargarCitas);