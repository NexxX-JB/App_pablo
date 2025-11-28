document.addEventListener("DOMContentLoaded", () => {
  const M = window.M // Variable de Materialize CSS
  const emociones = ["😊", "😢", "😠", "😰", "😌", "🤗"]
  let cartas = [...emociones, ...emociones]
  let cartasVolteadas = []
  let parejasEncontradas = 0
  let movimientos = 0
  let tiempoInicio = Date.now()
  let intervaloTiempo

  const tablero = document.getElementById("tableroJuego")
  const movimientosSpan = document.getElementById("movimientos")
  const parejasSpan = document.getElementById("parejas")
  const tiempoSpan = document.getElementById("tiempo")

  M.Modal.init(document.querySelectorAll(".modal"))

  iniciarJuego()

  document.getElementById("reiniciarJuego").addEventListener("click", () => {
    reiniciarJuego()
  })

  function iniciarJuego() {
    // Mezclar las cartas y reiniciar el tablero
    cartas = mezclarArreglo([...emociones, ...emociones])
    tablero.innerHTML = ""
    cartasVolteadas = []
    parejasEncontradas = 0
    movimientos = 0
    tiempoInicio = Date.now()

    movimientosSpan.textContent = movimientos
    parejasSpan.textContent = `0/${emociones.length}`

    // Crear cada carta en el tablero
    cartas.forEach((emocion, indice) => {
      const carta = document.createElement("div")
      carta.className = "carta"
      carta.dataset.indice = indice
      carta.dataset.emocion = emocion
      carta.innerHTML = `<span class="contenido">${emocion}</span>`

      carta.addEventListener("click", voltearCarta)
      tablero.appendChild(carta)
    })

    iniciarReloj()
  }

  function voltearCarta() {
    // No permitir voltear más de 2 cartas a la vez
    if (cartasVolteadas.length >= 2) return
    // No permitir voltear cartas ya volteadas o encontradas
    if (this.classList.contains("volteada") || this.classList.contains("encontrada")) return

    this.classList.add("volteada")
    cartasVolteadas.push(this)

    // Cuando hay 2 cartas volteadas, verificar si son pareja
    if (cartasVolteadas.length === 2) {
      movimientos++
      movimientosSpan.textContent = movimientos
      verificarPareja()
    }
  }

  function verificarPareja() {
    const [carta1, carta2] = cartasVolteadas

    // Si las emociones coinciden, marcar como encontradas
    if (carta1.dataset.emocion === carta2.dataset.emocion) {
      carta1.classList.add("encontrada")
      carta2.classList.add("encontrada")
      parejasEncontradas++
      parejasSpan.textContent = `${parejasEncontradas}/${emociones.length}`
      cartasVolteadas = []

      // Si se encontraron todas las parejas, juego completado
      if (parejasEncontradas === emociones.length) {
        setTimeout(juegoCompletado, 500)
      }
    } else {
      // Si no coinciden, voltear de nuevo después de 1 segundo
      setTimeout(() => {
        carta1.classList.remove("volteada")
        carta2.classList.remove("volteada")
        cartasVolteadas = []
      }, 1000)
    }
  }

  function juegoCompletado() {
    clearInterval(intervaloTiempo)
    const tiempoFinal = tiempoSpan.textContent

    document.getElementById("tiempoFinal").textContent = tiempoFinal
    document.getElementById("movimientosFinal").textContent = movimientos

    // Guardar puntos del juego
    let puntosJuegos = Number.parseInt(localStorage.getItem("puntosJuegos") || 0)
    puntosJuegos += 20
    localStorage.setItem("puntosJuegos", puntosJuegos)

    let juegosCompletados = Number.parseInt(localStorage.getItem("juegosCompletados") || 0)
    juegosCompletados++
    localStorage.setItem("juegosCompletados", juegosCompletados)

    // Agregar a puntos totales del usuario
    let puntosUsuario = Number.parseInt(localStorage.getItem("puntosUsuario") || 0)
    puntosUsuario += 20
    localStorage.setItem("puntosUsuario", puntosUsuario)

    // Mostrar modal de victoria
    const modal = M.Modal.getInstance(document.getElementById("modalVictoria"))
    modal.open()
  }

  function reiniciarJuego() {
    clearInterval(intervaloTiempo)
    iniciarJuego()
  }

  function iniciarReloj() {
    // Actualizar el tiempo cada segundo
    intervaloTiempo = setInterval(() => {
      const tiempoTranscurrido = Math.floor((Date.now() - tiempoInicio) / 1000)
      const minutos = Math.floor(tiempoTranscurrido / 60)
      const segundos = tiempoTranscurrido % 60
      tiempoSpan.textContent = `${minutos}:${segundos.toString().padStart(2, "0")}`
    }, 1000)
  }

  function mezclarArreglo(arreglo) {
    // Algoritmo Fisher-Yates para mezclar el arreglo
    for (let i = arreglo.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[arreglo[i], arreglo[j]] = [arreglo[j], arreglo[i]]
    }
    return arreglo
  }
})
