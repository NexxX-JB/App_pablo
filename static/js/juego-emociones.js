document.addEventListener("DOMContentLoaded", () => {
  const preguntas = [
    {
      situacion: "Tu mejor amigo te cuenta que consiguió el trabajo de sus sueños",
      respuesta: "Felicidad",
      opciones: ["Felicidad", "Tristeza", "Enojo", "Miedo"],
    },
    {
      situacion: "Perdiste algo muy importante para ti y no puedes encontrarlo",
      respuesta: "Tristeza",
      opciones: ["Alegría", "Tristeza", "Sorpresa", "Calma"],
    },
    {
      situacion: "Alguien te interrumpe constantemente mientras hablas",
      respuesta: "Enojo",
      opciones: ["Amor", "Enojo", "Felicidad", "Cansancio"],
    },
    {
      situacion: "Tienes que dar una presentación importante frente a muchas personas",
      respuesta: "Ansiedad",
      opciones: ["Ansiedad", "Alegría", "Aburrimiento", "Confianza"],
    },
    {
      situacion: "Estás en un lugar tranquilo, respirando profundamente y relajándote",
      respuesta: "Calma",
      opciones: ["Enojo", "Calma", "Sorpresa", "Tristeza"],
    },
  ]

  let preguntaActual = 0
  let puntos = 0
  let respuestasCorrectas = 0

  const situacionTexto = document.getElementById("situacionTexto")
  const opcionesContenedor = document.getElementById("opcionesContainer")
  const retroalimentacion = document.getElementById("feedback")
  const progreso = document.getElementById("progreso")
  const preguntaActualSpan = document.getElementById("preguntaActual")
  const totalPreguntasSpan = document.getElementById("totalPreguntas")
  const puntosActualesSpan = document.getElementById("puntosActuales")
  const juegoContenedor = document.getElementById("juegoContainer")
  const resultadoFinal = document.getElementById("resultadoFinal")

  totalPreguntasSpan.textContent = preguntas.length

  mostrarPregunta()

  document.getElementById("jugarOtraVez").addEventListener("click", () => {
    preguntaActual = 0
    puntos = 0
    respuestasCorrectas = 0
    juegoContenedor.style.display = "block"
    resultadoFinal.style.display = "none"
    mostrarPregunta()
  })

  function mostrarPregunta() {
    // Si ya no hay más preguntas, mostrar resultado
    if (preguntaActual >= preguntas.length) {
      mostrarResultado()
      return
    }

    const pregunta = preguntas[preguntaActual]
    situacionTexto.textContent = pregunta.situacion
    preguntaActualSpan.textContent = preguntaActual + 1

    // Actualizar barra de progreso
    const porcentaje = (preguntaActual / preguntas.length) * 100
    progreso.style.width = porcentaje + "%"

    opcionesContenedor.innerHTML = ""
    retroalimentacion.className = "feedback-message"

    // Crear botones de opciones
    pregunta.opciones.forEach((opcion) => {
      const boton = document.createElement("div")
      boton.className = "opcion-btn"
      boton.textContent = opcion
      boton.addEventListener("click", () => verificarRespuesta(opcion, pregunta.respuesta, boton))
      opcionesContenedor.appendChild(boton)
    })
  }

  function verificarRespuesta(seleccion, correcta, boton) {
    const botones = document.querySelectorAll(".opcion-btn")
    // Deshabilitar todos los botones después de seleccionar
    botones.forEach((btn) => btn.classList.add("disabled"))

    if (seleccion === correcta) {
      // Respuesta correcta
      boton.classList.add("correcta")
      retroalimentacion.className = "feedback-message correcto show"
      retroalimentacion.textContent = "¡Correcto! +3 puntos"
      puntos += 3
      respuestasCorrectas++
    } else {
      // Respuesta incorrecta
      boton.classList.add("incorrecta")
      retroalimentacion.className = "feedback-message incorrecto show"
      retroalimentacion.textContent = `Incorrecto. La respuesta correcta era: ${correcta}`

      // Mostrar la respuesta correcta en verde
      botones.forEach((btn) => {
        if (btn.textContent === correcta) {
          btn.classList.add("correcta")
        }
      })
    }

    puntosActualesSpan.textContent = puntos

    // Pasar a la siguiente pregunta después de 2.5 segundos
    setTimeout(() => {
      preguntaActual++
      mostrarPregunta()
    }, 2500)
  }

  function mostrarResultado() {
    juegoContenedor.style.display = "none"
    resultadoFinal.style.display = "block"

    document.getElementById("puntuacionFinal").textContent = puntos
    document.getElementById("correctas").textContent = respuestasCorrectas
    document.getElementById("totalRespuestas").textContent = preguntas.length

    // Guardar puntos en localStorage
    let puntosJuegos = Number.parseInt(localStorage.getItem("puntosJuegos") || 0)
    puntosJuegos += puntos
    localStorage.setItem("puntosJuegos", puntosJuegos)

    let juegosCompletados = Number.parseInt(localStorage.getItem("juegosCompletados") || 0)
    juegosCompletados++
    localStorage.setItem("juegosCompletados", juegosCompletados)

    // Agregar a puntos totales del usuario
    let puntosUsuario = Number.parseInt(localStorage.getItem("puntosUsuario") || 0)
    puntosUsuario += puntos
    localStorage.setItem("puntosUsuario", puntosUsuario)
  }
})
