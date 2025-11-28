-- Script para crear la base de datos MySQL del sistema de emociones
-- Primero crea la base de datos
CREATE DATABASE IF NOT EXISTS sistema_emociones CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE sistema_emociones;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) UNIQUE NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    codigo_verificacion VARCHAR(10),
    verificado TINYINT(1) DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL DEFAULT NULL,
    INDEX idx_usuarios_nombre (nombre_usuario),
    INDEX idx_usuarios_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de avatares
CREATE TABLE IF NOT EXISTS avatares_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    emoji_avatar VARCHAR(10) NOT NULL,
    fecha_seleccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_avatares_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de puntos
CREATE TABLE IF NOT EXISTS puntos_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    puntos_totales INT DEFAULT 0,
    puntos_gastados INT DEFAULT 0,
    puntos_disponibles INT DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_puntos_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de misiones
CREATE TABLE IF NOT EXISTS misiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    icono VARCHAR(10) NOT NULL,
    puntos_recompensa INT NOT NULL,
    activa TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de misiones completadas por usuario
CREATE TABLE IF NOT EXISTS misiones_completadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mision_id INT NOT NULL,
    fecha_completada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntos_ganados INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE,
    INDEX idx_misiones_completadas_usuario (usuario_id),
    INDEX idx_misiones_completadas_fecha (fecha_completada)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de recompensas disponibles
CREATE TABLE IF NOT EXISTS recompensas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    icono VARCHAR(10) NOT NULL,
    costo_puntos INT NOT NULL,
    activa TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de recompensas reclamadas
CREATE TABLE IF NOT EXISTS recompensas_reclamadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    recompensa_id INT NOT NULL,
    fecha_reclamada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntos_gastados INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (recompensa_id) REFERENCES recompensas(id) ON DELETE CASCADE,
    INDEX idx_recompensas_reclamadas_usuario (usuario_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de historial de actividades
CREATE TABLE IF NOT EXISTS historial_actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo_actividad VARCHAR(100) NOT NULL,
    descripcion TEXT,
    puntos_cambio INT DEFAULT 0,
    fecha_actividad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_historial_usuario (usuario_id),
    INDEX idx_historial_fecha (fecha_actividad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de juegos jugados
CREATE TABLE IF NOT EXISTS juegos_jugados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre_juego VARCHAR(100) NOT NULL,
    puntuacion INT NOT NULL,
    tiempo_jugado INT,
    fecha_juego TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_juegos_usuario (usuario_id),
    INDEX idx_juegos_fecha (fecha_juego)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
