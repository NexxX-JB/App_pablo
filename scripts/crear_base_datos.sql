-- Script para crear la base de datos del sistema de emociones
-- Tablas: usuarios, avatares, puntos, misiones, recompensas, historial

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    codigo_verificacion TEXT,
    verificado INTEGER DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP
);

-- Tabla de avatares
CREATE TABLE IF NOT EXISTS avatares_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    emoji_avatar TEXT NOT NULL,
    fecha_seleccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de puntos
CREATE TABLE IF NOT EXISTS puntos_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    puntos_totales INTEGER DEFAULT 0,
    puntos_gastados INTEGER DEFAULT 0,
    puntos_disponibles INTEGER DEFAULT 0,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de misiones
CREATE TABLE IF NOT EXISTS misiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    categoria TEXT NOT NULL,
    icono TEXT NOT NULL,
    puntos_recompensa INTEGER NOT NULL,
    activa INTEGER DEFAULT 1
);

-- Tabla de misiones completadas por usuario
-- Eliminada la expresión DATE() de la restricción UNIQUE
CREATE TABLE IF NOT EXISTS misiones_completadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    mision_id INTEGER NOT NULL,
    fecha_completada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntos_ganados INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE
);

-- Tabla de recompensas disponibles
CREATE TABLE IF NOT EXISTS recompensas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    icono TEXT NOT NULL,
    costo_puntos INTEGER NOT NULL,
    activa INTEGER DEFAULT 1
);

-- Tabla de recompensas reclamadas
CREATE TABLE IF NOT EXISTS recompensas_reclamadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    recompensa_id INTEGER NOT NULL,
    fecha_reclamada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntos_gastados INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (recompensa_id) REFERENCES recompensas(id) ON DELETE CASCADE
);

-- Tabla de historial de actividades
CREATE TABLE IF NOT EXISTS historial_actividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo_actividad TEXT NOT NULL,
    descripcion TEXT,
    puntos_cambio INTEGER DEFAULT 0,
    fecha_actividad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de juegos jugados
CREATE TABLE IF NOT EXISTS juegos_jugados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre_juego TEXT NOT NULL,
    puntuacion INTEGER NOT NULL,
    tiempo_jugado INTEGER,
    fecha_juego TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_usuarios_nombre ON usuarios(nombre_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);
CREATE INDEX IF NOT EXISTS idx_avatares_usuario ON avatares_usuario(usuario_id);
CREATE INDEX IF NOT EXISTS idx_puntos_usuario ON puntos_usuario(usuario_id);
CREATE INDEX IF NOT EXISTS idx_misiones_completadas_usuario ON misiones_completadas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_recompensas_reclamadas_usuario ON recompensas_reclamadas(usuario_id);
CREATE INDEX IF NOT EXISTS idx_historial_usuario ON historial_actividades(usuario_id);
CREATE INDEX IF NOT EXISTS idx_juegos_usuario ON juegos_jugados(usuario_id);
