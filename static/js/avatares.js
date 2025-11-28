const M = window.M // Variable de Materialize CSS

document.addEventListener("DOMContentLoaded", () => {
  M.Sidenav.init(document.querySelectorAll(".sidenav"))

  const avatarActual = document.getElementById("avatarActual")
  const avatarNombre = document.getElementById("avatarNombre")
  const tarjetasAvatar = document.querySelectorAll(".avatar-card")
  const botonGuardar = document.getElementById("guardarAvatar")
  const botonEliminar = document.getElementById("eliminarAvatar")

  let avatarSeleccionado = {
    emoji: "😊",
    nombre: "Feliz",
    emocion: "felicidad",
  }

  // Cargar avatar guardado desde localStorage
  const avatarGuardado = localStorage.getItem("avatarActual")
  if (avatarGuardado) {
    const datos = JSON.parse(avatarGuardado)
    avatarSeleccionado = datos
    avatarActual.textContent = datos.emoji
    avatarNombre.textContent = datos.nombre
  }

  // Seleccionar avatar al hacer clic
  tarjetasAvatar.forEach((tarjeta) => {
    // Marcar el avatar actual como seleccionado
    if (tarjeta.dataset.avatar === avatarSeleccionado.emoji) {
      tarjeta.classList.add("selected")
    }

    tarjeta.addEventListener("click", function () {
      // Remover selección de todas las tarjetas
      tarjetasAvatar.forEach((t) => t.classList.remove("selected"))
      // Marcar esta tarjeta como seleccionada
      this.classList.add("selected")

      avatarSeleccionado = {
        emoji: this.dataset.avatar,
        nombre: this.dataset.nombre,
        emocion: this.dataset.emocion,
      }

      avatarActual.textContent = avatarSeleccionado.emoji
      avatarNombre.textContent = avatarSeleccionado.nombre
    })
  })

  // Guardar avatar seleccionado
  botonGuardar.addEventListener("click", () => {
    localStorage.setItem("avatarActual", JSON.stringify(avatarSeleccionado))

    // Registrar actividad en el historial
    const actividad = `Avatar cambiado a: ${avatarSeleccionado.nombre}`
    agregarActividad(actividad)

    M.toast({ html: `¡Avatar "${avatarSeleccionado.nombre}" guardado!`, classes: "green" })
  })

  // Eliminar avatar y usar el predeterminado
  botonEliminar.addEventListener("click", () => {
    avatarSeleccionado = {
      emoji: "😊",
      nombre: "Feliz",
      emocion: "felicidad",
    }

    avatarActual.textContent = avatarSeleccionado.emoji
    avatarNombre.textContent = avatarSeleccionado.nombre
    localStorage.setItem("avatarActual", JSON.stringify(avatarSeleccionado))

    // Marcar el primer avatar como seleccionado
    tarjetasAvatar.forEach((t) => t.classList.remove("selected"))
    tarjetasAvatar[0].classList.add("selected")

    M.toast({ html: "Avatar predeterminado restaurado", classes: "orange" })
  })

  function agregarActividad(mensaje) {
    // Guardar actividad en el historial
    const historial = JSON.parse(localStorage.getItem("historialActividades")) || []
    const fecha = new Date().toLocaleString()
    historial.push(`${fecha}: ${mensaje}`)
    localStorage.setItem("historialActividades", JSON.stringify(historial))
  }
})
