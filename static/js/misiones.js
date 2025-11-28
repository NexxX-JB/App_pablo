const M = window.M

document.addEventListener("DOMContentLoaded", () => {
  M.Sidenav.init(document.querySelectorAll(".sidenav"))

  const casillasVerificacion = document.querySelectorAll(".mision-checkbox")
  const puntosHoySpan = document.getElementById("puntosHoy")
  const misionesCompletadasSpan = document.getElementById("misionesCompletadas")
  const totalMisionesSpan = document.getElementById("totalMisiones")

  let puntosHoy = 0
  let misionesCompletadas = 0

  cargarEstadoMisiones()

  casillasVerificacion.forEach((casilla) => {
    casilla.addEventListener("change", function () {
      const tarjetaMision = this.closest(".mision-card")
      const puntos = Number.parseInt(tarjetaMision.dataset.puntos)
      const misionId = tarjetaMision.dataset.mision

      if (this.checked) {
        const usuarioId = localStorage.getItem("usuarioId")

        if (!usuarioId) {
          M.toast({ html: "Debes iniciar sesión para completar misiones", classes: "red" })
          this.checked = false
          return
        }

        fetch("/api/completar-mision", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            usuario_id: usuarioId,
            mision_id: misionId,
          }),
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.exito) {
              // Misión completada exitosamente
              tarjetaMision.classList.add("completada")
              puntosHoy += puntos
              misionesCompletadas++
              actualizarEstadisticas()

              M.toast({ html: data.mensaje, classes: "green" })

              casilla.disabled = true
              tarjetaMision.style.opacity = "0.6"

              // Guardar tiempo de bloqueo en localStorage
              const tiempoBloqueo = {
                misionId: misionId,
                fechaCompletada: new Date().toISOString(),
              }

              let misionesBloqueadas = JSON.parse(localStorage.getItem("misionesBloqueadas") || "[]")
              misionesBloqueadas = misionesBloqueadas.filter((m) => m.misionId !== misionId)
              misionesBloqueadas.push(tiempoBloqueo)
              localStorage.setItem("misionesBloqueadas", JSON.stringify(misionesBloqueadas))
            } else {
              // Error al completar misión
              this.checked = false
              M.toast({ html: data.mensaje, classes: "orange" })
            }
          })
          .catch((error) => {
            console.error("Error al completar misión:", error)
            this.checked = false
            M.toast({ html: "Error al completar misión", classes: "red" })
          })
      } else {
        // No permitir desmarcar misiones completadas
        M.toast({ html: "No puedes desmarcar misiones completadas", classes: "orange" })
        this.checked = true
      }
    })
  })

  function cargarEstadoMisiones() {
    const misionesBloqueadas = JSON.parse(localStorage.getItem("misionesBloqueadas") || "[]")
    const ahora = new Date()
    const misionesBloqueadasActualizadas = []

    misionesBloqueadas.forEach((bloqueo) => {
      const fechaCompletada = new Date(bloqueo.fechaCompletada)
      const horasTranscurridas = (ahora - fechaCompletada) / (1000 * 60 * 60)

      if (horasTranscurridas < 24) {
        // Todavía está bloqueada
        const tarjetaMision = document.querySelector(`[data-mision="${bloqueo.misionId}"]`)
        if (tarjetaMision) {
          const casilla = tarjetaMision.querySelector(".mision-checkbox")
          casilla.checked = true
          casilla.disabled = true
          tarjetaMision.classList.add("completada")
          tarjetaMision.style.opacity = "0.6"

          const horasRestantes = Math.floor(24 - horasTranscurridas)
          const minutosRestantes = Math.floor(((24 - horasTranscurridas) % 1) * 60)

          // Agregar indicador de tiempo
          const indicadorTiempo = document.createElement("div")
          indicadorTiempo.className = "tiempo-restante"
          indicadorTiempo.style.cssText = "font-size: 12px; color: #ff6f00; margin-top: 5px;"
          indicadorTiempo.textContent = `Disponible en: ${horasRestantes}h ${minutosRestantes}m`
          tarjetaMision.appendChild(indicadorTiempo)
        }

        misionesBloqueadasActualizadas.push(bloqueo)
      }
    })

    // Actualizar localStorage con solo las misiones que siguen bloqueadas
    localStorage.setItem("misionesBloqueadas", JSON.stringify(misionesBloqueadasActualizadas))

    actualizarEstadisticas()
  }

  function actualizarEstadisticas() {
    puntosHoySpan.textContent = puntosHoy
    misionesCompletadasSpan.textContent = misionesCompletadas
    totalMisionesSpan.textContent = casillasVerificacion.length
  }
})
