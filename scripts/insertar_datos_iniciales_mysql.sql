-- Script para insertar datos iniciales en MySQL
USE sistema_emociones;

-- Insertar misiones predefinidas
INSERT INTO misiones (titulo, descripcion, categoria, icono, puntos_recompensa) VALUES
('Registra tu emoción del día', 'Identifica y registra cómo te sientes hoy', 'Diarias', '📝', 5),
('Completa un ejercicio de respiración', 'Practica respiración profunda por 5 minutos', 'Diarias', '🧘', 5),
('Escribe en tu diario', 'Escribe sobre tu día y tus emociones', 'Diarias', '📖', 5),
('Juega un mini juego', 'Completa cualquier mini juego disponible', 'Semanales', '🎮', 10),
('Identifica 3 emociones diferentes', 'Reconoce y nombra 3 emociones distintas', 'Semanales', '🎭', 10),
('Comparte tu progreso', 'Comparte tu avance con alguien de confianza', 'Semanales', '💬', 10),
('Completa 7 días seguidos', 'Mantén una racha de 7 días consecutivos', 'Especiales', '🔥', 20),
('Alcanza 100 puntos', 'Acumula un total de 100 puntos', 'Especiales', '⭐', 20),
('Maestro de emociones', 'Completa todas las misiones diarias y semanales', 'Especiales', '🏆', 30);

-- Insertar recompensas predefinidas
INSERT INTO recompensas (titulo, descripcion, icono, costo_puntos) VALUES
('Avatar Premium', 'Desbloquea avatares exclusivos premium', '👑', 50),
('Insignia de Bronce', 'Obtén la insignia de bronce por tu progreso', '🥉', 25),
('Insignia de Plata', 'Obtén la insignia de plata por tu dedicación', '🥈', 50),
('Insignia de Oro', 'Obtén la insignia de oro por tu excelencia', '🥇', 100),
('Certificado de Logro', 'Descarga tu certificado de logro personalizado', '📜', 75);
