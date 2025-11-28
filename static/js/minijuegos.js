// Esperar a que el documento esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  const M = window.M // Declarar la variable M antes de usarla
  M.Sidenav.init(document.querySelectorAll(".sidenav"))

  // Cargar estadísticas de juegos
  cargarEstadisticas()
})

// Función para cargar y mostrar las estadísticas de los juegos
function cargarEstadisticas() {
  const puntos = localStorage.getItem("puntosJuegos") || 0
  const completados = localStorage.getItem("juegosCompletados") || 0

  document.getElementById("puntosJuegos").textContent = puntos
  document.getElementById("juegosCompletados").textContent = completados
}
