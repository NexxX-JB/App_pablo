document.addEventListener("DOMContentLoaded", () => {
  const M = window.M // Variable de Materialize CSS
  M.Sidenav.init(document.querySelectorAll(".sidenav"))
  M.Modal.init(document.querySelectorAll(".modal"))

  const puntosDisponiblesSpan = document.getElementById("puntosDisponibles")
  const historialContenedor = document.getElementById("historialRecompensas")
  const botonesReclamar = document.querySelectorAll(".btn-reclamar")

  cargarPuntos()
  cargarHistorial()

  botonesReclamar.forEach((boton) => {
    boton.addEventListener("click", function () {
      const tarjeta = this.closest(".recompensa-card")
      const recompensaId = tarjeta.dataset.id
      const costo = Number.parseInt(tarjeta.dataset.costo)

      reclamarRecompensa(recompensaId, costo, tarjeta)
    })
  })

  function cargarPuntos() {
    // Cargar puntos disponibles del usuario
    const puntos = Number.parseInt(localStorage.getItem("puntosUsuario") || 0)
    puntosDisponiblesSpan.textContent = puntos

    // Deshabilitar botones si no hay suficientes puntos
    botonesReclamar.forEach((boton) => {
      const tarjeta = boton.closest(".recompensa-card")
      const costo = Number.parseInt(tarjeta.dataset.costo)

      if (puntos < costo) {
        boton.classList.add("disabled")
        boton.textContent = "Puntos insuficientes"
      }

      // Verificar si ya fue reclamada
      const recompensasReclamadas = JSON.parse(localStorage.getItem("recompensasReclamadas") || "[]")
      if (recompensasReclamadas.includes(tarjeta.dataset.id)) {
        tarjeta.classList.add("reclamada")
        boton.classList.add("disabled")
        boton.innerHTML = '<i class="material-icons left">check</i>Reclamada'
      }
    })
  }

  function reclamarRecompensa(recompensaId, costo, tarjeta) {
    const puntosActuales = Number.parseInt(localStorage.getItem("puntosUsuario") || 0)

    // Verificar si hay puntos suficientes
    if (puntosActuales < costo) {
      mostrarError("No tienes suficientes puntos para esta recompensa")
      return
    }

    // Verificar si ya fue reclamada
    const recompensasReclamadas = JSON.parse(localStorage.getItem("recompensasReclamadas") || "[]")
    if (recompensasReclamadas.includes(recompensaId)) {
      mostrarError("Esta recompensa ya ha sido reclamada")
      return
    }

    // Reclamar recompensa y restar puntos
    const nuevosPuntos = puntosActuales - costo
    localStorage.setItem("puntosUsuario", nuevosPuntos)

    recompensasReclamadas.push(recompensaId)
    localStorage.setItem("recompensasReclamadas", JSON.stringify(recompensasReclamadas))

    // Guardar en historial
    const historial = JSON.parse(localStorage.getItem("historialRecompensas") || "[]")
    const nombreRecompensa = tarjeta.querySelector("h6").textContent
    historial.push({
      id: recompensaId,
      nombre: nombreRecompensa,
      costo: costo,
      fecha: new Date().toLocaleString(),
    })
    localStorage.setItem("historialRecompensas", JSON.stringify(historial))

    // Actualizar interfaz
    puntosDisponiblesSpan.textContent = nuevosPuntos
    tarjeta.classList.add("reclamada")
    const boton = tarjeta.querySelector(".btn-reclamar")
    boton.classList.add("disabled")
    boton.innerHTML = '<i class="material-icons left">check</i>Reclamada'

    // Mostrar modal de éxito
    document.getElementById("mensajeExito").textContent = `Has reclamado: ${nombreRecompensa}`
    document.getElementById("puntosRestantes").textContent = nuevosPuntos
    const modal = M.Modal.getInstance(document.getElementById("modalExito"))
    modal.open()

    cargarHistorial()
    cargarPuntos()
  }

  function cargarHistorial() {
    // Cargar historial de recompensas reclamadas
    const historial = JSON.parse(localStorage.getItem("historialRecompensas") || "[]")

    if (historial.length === 0) {
      historialContenedor.innerHTML = '<p class="center-align grey-text">No has reclamado ninguna recompensa aún</p>'
      return
    }

    historialContenedor.innerHTML = ""
    // Mostrar las recompensas más recientes primero
    historial.reverse().forEach((item) => {
      const div = document.createElement("div")
      div.className = "historial-item"
      div.innerHTML = `
                <div class="historial-icon">
                    <i class="material-icons">card_giftcard</i>
                </div>
                <div class="historial-info">
                    <h6>${item.nombre}</h6>
                    <p>${item.fecha} • ${item.costo} puntos</p>
                </div>
            `
      historialContenedor.appendChild(div)
    })
  }

  function mostrarError(mensaje) {
    // Mostrar modal de error
    document.getElementById("mensajeError").textContent = mensaje
    const modal = M.Modal.getInstance(document.getElementById("modalError"))
    modal.open()
  }
})
