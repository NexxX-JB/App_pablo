// Declare the M variable or import it as needed
const M = window.M // Variable de Materialize CSS

document.addEventListener("DOMContentLoaded", () => {
  M.Sidenav.init(document.querySelectorAll(".sidenav"))

  cargarPerfil()
})

function cargarPerfil() {
  // Cargar avatar del usuario
  const avatarGuardado = localStorage.getItem("avatarActual")
  if (avatarGuardado) {
    const datos = JSON.parse(avatarGuardado)
    document.getElementById("avatarPerfil").textContent = datos.emoji
  }

  // Cargar nombre del usuario
  const nombre = localStorage.getItem("nombreUsuario") || "Usuario"
  document.getElementById("nombreUsuario").textContent = nombre

  // Cargar estadísticas del usuario
  const puntosTotales = Number.parseInt(localStorage.getItem("puntosUsuario") || 0)
  const misionesCompletadas = JSON.parse(localStorage.getItem("misionesCompletadas") || "[]").length
  const recompensasReclamadas = JSON.parse(localStorage.getItem("recompensasReclamadas") || "[]").length

  document.getElementById("totalPuntos").textContent = puntosTotales
  document.getElementById("misionesTotal").textContent = misionesCompletadas
  document.getElementById("recompensasTotal").textContent = recompensasReclamadas
}
