from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import hashlib
import random
import string
import os
from dotenv import load_dotenv

aplicacion = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
aplicacion.secret_key = 'tu_clave_secreta_super_segura_2025'



load_dotenv()  # Solo si quieres cargar .env local, no obligatorio en Railway

MYSQL_CONFIG = {
    
    'host': 'caboose.proxy.rlwy.net',
    'user': 'root',
    'password': 'pBpINcrdIOAVjcKovMdnDGKuonTLaIOB',
    'database': 'railway',
    'port': 56390,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
def obtener_conexion_bd():
    """Crea y retorna una conexión a la base de datos MySQL"""
    try:
        conexion = mysql.connector.connect(**MYSQL_CONFIG)
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def inicializar_bd():
    """Inicializa la base de datos ejecutando los scripts SQL de MySQL"""
    try:
        # Conectar sin especificar base de datos para crearla
        conexion_temp = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conexion_temp.cursor()
        
        # Leer y ejecutar el script de creación de tablas
        ruta_script_crear = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'crear_base_datos_mysql.sql')
        if os.path.exists(ruta_script_crear):
            with open(ruta_script_crear, 'r', encoding='utf-8') as archivo:
                script_sql = archivo.read()
                # Ejecutar cada sentencia SQL individualmente
                for sentencia in script_sql.split(';'):
                    if sentencia.strip():
                        cursor.execute(sentencia)
        
        conexion_temp.commit()
        conexion_temp.close()
        
        # Ahora conectar a la base de datos creada
        conexion = obtener_conexion_bd()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            
            # Verificar si ya hay datos iniciales
            cursor.execute("SELECT COUNT(*) as total FROM misiones")
            resultado = cursor.fetchone()
            
            if resultado['total'] == 0:
                # Leer y ejecutar el script de datos iniciales
                ruta_script_datos = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'insertar_datos_iniciales_mysql.sql')
                if os.path.exists(ruta_script_datos):
                    with open(ruta_script_datos, 'r', encoding='utf-8') as archivo:
                        script_sql = archivo.read()
                        for sentencia in script_sql.split(';'):
                            if sentencia.strip():
                                cursor.execute(sentencia)
            
            conexion.commit()
            conexion.close()
            print("Base de datos MySQL inicializada correctamente")
    except Error as e:
        print(f"Error al inicializar la base de datos: {e}")

def encriptar_contrasena(contrasena):
    """Encripta una contraseña usando SHA-256"""
    return hashlib.sha256(contrasena.encode()).hexdigest()

# Inicializar la base de datos al iniciar la aplicación
inicializar_bd()

@aplicacion.route("/")
def pagina_principal():
    return render_template("index.html")

@aplicacion.route("/avatares")
def avatares():
    return render_template("avatares.html")

@aplicacion.route("/minijuegos")
def minijuegos():
    return render_template("minijuegos.html")

@aplicacion.route("/juego-memoria")
def juego_memoria():
    return render_template("juego-memoria.html")

@aplicacion.route("/juego-emociones")
def juego_emociones():
    return render_template("juego-emociones.html")

@aplicacion.route("/misiones")
def misiones():
    return render_template("misiones.html")

@aplicacion.route("/recompensas")
def recompensas():
    return render_template("recompensas.html")

@aplicacion.route("/perfil")
def perfil():
    return render_template("perfil.html")

@aplicacion.route("/historial")
def historial():
    """Página de historial de actividades"""
    return render_template('historial.html')

@aplicacion.route("/api/registro", methods=["POST"])
def registrar_usuario():
    """Registra un nuevo usuario en la base de datos"""
    try:
        datos = request.json
        nombre_usuario = datos.get('nombre_usuario')
        correo = datos.get('correo')
        contrasena = datos.get('contrasena')
        
        print(f"[v0] Intentando registrar usuario: {nombre_usuario}, correo: {correo}")
        
        # Validaciones
        if not nombre_usuario or not correo or not contrasena:
            return jsonify({"exito": False, "mensaje": "Todos los campos son obligatorios"}), 400
        
        contrasena_encriptada = encriptar_contrasena(contrasena)
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión a la base de datos"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s OR correo = %s", 
                      (nombre_usuario, correo))
        usuario_existente = cursor.fetchone()
        
        if usuario_existente:
            conexion.close()
            print(f"[v0] Usuario ya existe: {nombre_usuario} o correo: {correo}")
            return jsonify({"exito": False, "mensaje": "El nombre de usuario o correo ya está registrado"}), 400
        
        cursor.execute("""
            INSERT INTO usuarios (nombre_usuario, correo, contrasena, verificado)
            VALUES (%s, %s, %s, 1)
        """, (nombre_usuario, correo, contrasena_encriptada))
        
        usuario_id = cursor.lastrowid
        
        # Inicializar puntos del usuario
        cursor.execute("""
            INSERT INTO puntos_usuario (usuario_id, puntos_totales, puntos_gastados, puntos_disponibles)
            VALUES (%s, 0, 0, 0)
        """, (usuario_id,))
        
        conexion.commit()
        conexion.close()
        
        print(f"[v0] Usuario registrado exitosamente con ID: {usuario_id}")
        
        return jsonify({
            "exito": True,
            "mensaje": "Registro exitoso",
            "usuario_id": usuario_id
        })
        
    except Error as e:
        print(f"[v0] Error en registro: {e}")
        return jsonify({"exito": False, "mensaje": f"Error en el registro: {str(e)}"}), 500

@aplicacion.route("/api/login", methods=["POST"])
def iniciar_sesion():
    """Inicia sesión con usuario y contraseña"""
    try:
        datos = request.json
        nombre_usuario = datos.get('nombre_usuario')
        contrasena = datos.get('contrasena')
        
        print(f"[v0] Intentando login: {nombre_usuario}")
        
        if not nombre_usuario or not contrasena:
            return jsonify({"exito": False, "mensaje": "Usuario y contraseña son obligatorios"}), 400
        
        contrasena_encriptada = encriptar_contrasena(contrasena)
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, nombre_usuario FROM usuarios 
            WHERE nombre_usuario = %s AND contrasena = %s
        """, (nombre_usuario, contrasena_encriptada))
        
        usuario = cursor.fetchone()
        
        if not usuario:
            conexion.close()
            print(f"[v0] Login fallido: Usuario o contraseña incorrectos")
            return jsonify({"exito": False, "mensaje": "Usuario o contraseña incorrectos"}), 401
        
        # Actualizar último acceso
        cursor.execute("UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = %s", (usuario['id'],))
        conexion.commit()
        
        # Obtener puntos del usuario
        cursor.execute("""
            SELECT puntos_disponibles FROM puntos_usuario WHERE usuario_id = %s
        """, (usuario['id'],))
        
        puntos = cursor.fetchone()
        puntos_disponibles = puntos['puntos_disponibles'] if puntos else 0
        
        conexion.close()
        
        print(f"[v0] Login exitoso para usuario ID: {usuario['id']}")
        
        return jsonify({
            "exito": True,
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario['id'],
                "nombre_usuario": usuario['nombre_usuario'],
                "puntos": puntos_disponibles
            }
        })
        
    except Error as e:
        print(f"[v0] Error en login: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/cerrar-sesion", methods=["POST"])
def cerrar_sesion():
    """Cierra la sesión del usuario"""
    session.clear()
    return jsonify({"exito": True, "mensaje": "Sesión cerrada"})

@aplicacion.route("/api/guardar-avatar", methods=["POST"])
def guardar_avatar():
    """Guarda el avatar seleccionado por el usuario"""
    datos = request.json
    usuario_id = datos.get('usuario_id')
    emoji_avatar = datos.get('avatar')
    
    if not usuario_id or not emoji_avatar:
        return jsonify({"exito": False, "mensaje": "Datos incompletos"})
    
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        # Desactivar avatar anterior
        cursor.execute("UPDATE avatares_usuario SET activo = 0 WHERE usuario_id = %s", (usuario_id,))
        
        # Insertar nuevo avatar
        cursor.execute("""
            INSERT INTO avatares_usuario (usuario_id, emoji_avatar, activo)
            VALUES (%s, %s, 1)
        """, (usuario_id, emoji_avatar))
        
        # Registrar en historial
        cursor.execute("""
            INSERT INTO historial_actividades (usuario_id, tipo_actividad, descripcion)
            VALUES (%s, 'avatar', 'Cambió su avatar')
        """, (usuario_id,))
        
        conexion.commit()
        return jsonify({"exito": True, "avatar": emoji_avatar})
        
    except Error as e:
        conexion.rollback()
        return jsonify({"exito": False, "mensaje": f"Error: {str(e)}"})
    finally:
        conexion.close()

@aplicacion.route("/api/obtener-avatar/<int:usuario_id>")
def obtener_avatar(usuario_id):
    """Obtiene el avatar activo del usuario"""
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT emoji_avatar FROM avatares_usuario 
            WHERE usuario_id = %s AND activo = 1
            ORDER BY fecha_seleccion DESC LIMIT 1
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            return jsonify({"avatar": resultado['emoji_avatar']})
        else:
            return jsonify({"avatar": "😊"})  # Avatar predeterminado
            
    finally:
        conexion.close()

@aplicacion.route("/api/eliminar-avatar", methods=["POST"])
def eliminar_avatar():
    """Elimina el avatar del usuario y vuelve al predeterminado"""
    datos = request.json
    usuario_id = datos.get('usuario_id')
    
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("UPDATE avatares_usuario SET activo = 0 WHERE usuario_id = %s", (usuario_id,))
        
        cursor.execute("""
            INSERT INTO historial_actividades (usuario_id, tipo_actividad, descripcion)
            VALUES (%s, 'avatar', 'Eliminó su avatar personalizado')
        """, (usuario_id,))
        
        conexion.commit()
        return jsonify({"exito": True, "mensaje": "Avatar eliminado"})
        
    finally:
        conexion.close()

@aplicacion.route("/api/guardar-progreso", methods=["POST"])
def guardar_progreso():
    """Guarda el progreso del juego y actualiza puntos"""
    try:
        datos = request.json
        usuario_id = datos.get('usuario_id')
        tipo = datos.get('tipo')
        puntos = datos.get('puntos', 0)
        
        if not usuario_id:
            return jsonify({"exito": False, "mensaje": "ID de usuario requerido"}), 400
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Actualizar puntos del usuario
        if puntos > 0:
            cursor.execute("""
                UPDATE puntos_usuario 
                SET puntos_totales = puntos_totales + %s,
                    puntos_disponibles = puntos_disponibles + %s
                WHERE usuario_id = %s
            """, (puntos, puntos, usuario_id))
            
            # Registrar en historial
            cursor.execute("""
                INSERT INTO historial_actividades (usuario_id, tipo_actividad, descripcion, puntos_cambio)
                VALUES (%s, %s, %s, %s)
            """, (usuario_id, 'Juego Completado', tipo, puntos))
        
        conexion.commit()
        conexion.close()
        
        return jsonify({"exito": True, "mensaje": "Progreso guardado"})
        
    except Error as e:
        print(f"Error al guardar progreso: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/obtener-puntos/<int:usuario_id>")
def obtener_puntos(usuario_id):
    """Obtiene los puntos del usuario"""
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT puntos_totales, puntos_disponibles, puntos_gastados 
            FROM puntos_usuario 
            WHERE usuario_id = %s
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            return jsonify({
                "puntos_totales": resultado['puntos_totales'],
                "puntos_disponibles": resultado['puntos_disponibles'],
                "puntos_gastados": resultado['puntos_gastados']
            })
        else:
            return jsonify({
                "puntos_totales": 0,
                "puntos_disponibles": 0,
                "puntos_gastados": 0
            })
            
    finally:
        conexion.close()

@aplicacion.route("/api/misiones")
def obtener_misiones():
    """Obtiene todas las misiones disponibles y su estado para el usuario"""
    try:
        usuario_id = request.args.get('usuario_id')
        
        if not usuario_id:
            return jsonify({"exito": False, "mensaje": "ID de usuario requerido"}), 400
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Obtener todas las misiones activas
        cursor.execute("SELECT * FROM misiones WHERE activa = 1")
        misiones = cursor.fetchall()
        
        # Para cada misión, verificar si fue completada en las últimas 24 horas
        for mision in misiones:
            cursor.execute("""
                SELECT fecha_completada, 
                       TIMESTAMPDIFF(SECOND, fecha_completada, NOW()) as segundos_transcurridos
                FROM misiones_completadas 
                WHERE usuario_id = %s AND mision_id = %s 
                ORDER BY fecha_completada DESC 
                LIMIT 1
            """, (usuario_id, mision['id']))
            
            completada = cursor.fetchone()
            
            if completada:
                segundos_transcurridos = completada['segundos_transcurridos']
                segundos_en_24h = 24 * 60 * 60
                
                if segundos_transcurridos < segundos_en_24h:
                    # Aún no han pasado 24 horas
                    mision['completada'] = True
                    mision['tiempo_restante'] = segundos_en_24h - segundos_transcurridos
                else:
                    # Ya pasaron 24 horas, puede reclamar de nuevo
                    mision['completada'] = False
                    mision['tiempo_restante'] = 0
            else:
                mision['completada'] = False
                mision['tiempo_restante'] = 0
        
        conexion.close()
        return jsonify({"exito": True, "misiones": misiones})
        
    except Error as e:
        print(f"Error al obtener misiones: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/completar-mision", methods=["POST"])
def completar_mision():
    """Marca una misión como completada y otorga puntos al usuario"""
    try:
        datos = request.json
        usuario_id = datos.get('usuario_id')
        mision_id = datos.get('mision_id')
        
        if not usuario_id or not mision_id:
            return jsonify({"exito": False, "mensaje": "Datos incompletos"}), 400
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si ya completó esta misión en las últimas 24 horas
        cursor.execute("""
            SELECT fecha_completada,
                   TIMESTAMPDIFF(SECOND, fecha_completada, NOW()) as segundos_transcurridos
            FROM misiones_completadas 
            WHERE usuario_id = %s AND mision_id = %s 
            ORDER BY fecha_completada DESC 
            LIMIT 1
        """, (usuario_id, mision_id))
        
        ultima_completada = cursor.fetchone()
        
        if ultima_completada:
            segundos_transcurridos = ultima_completada['segundos_transcurridos']
            if segundos_transcurridos < (24 * 60 * 60):
                tiempo_restante = (24 * 60 * 60) - segundos_transcurridos
                conexion.close()
                return jsonify({
                    "exito": False,
                    "mensaje": "Ya completaste esta misión hoy",
                    "tiempo_restante": tiempo_restante
                }), 400
        
        # Obtener información de la misión
        cursor.execute("SELECT * FROM misiones WHERE id = %s", (mision_id,))
        mision = cursor.fetchone()
        
        if not mision:
            conexion.close()
            return jsonify({"exito": False, "mensaje": "Misión no encontrada"}), 404
        
        # Registrar misión completada
        cursor.execute("""
            INSERT INTO misiones_completadas (usuario_id, mision_id, puntos_ganados)
            VALUES (%s, %s, %s)
        """, (usuario_id, mision_id, mision['puntos_recompensa']))
        
        # Actualizar puntos del usuario
        cursor.execute("""
            UPDATE puntos_usuario 
            SET puntos_totales = puntos_totales + %s,
                puntos_disponibles = puntos_disponibles + %s
            WHERE usuario_id = %s
        """, (mision['puntos_recompensa'], mision['puntos_recompensa'], usuario_id))
        
        # Registrar en historial
        cursor.execute("""
            INSERT INTO historial_actividades (usuario_id, tipo_actividad, descripcion, puntos_cambio)
            VALUES (%s, 'Misión Completada', %s, %s)
        """, (usuario_id, mision['titulo'], mision['puntos_recompensa']))
        
        conexion.commit()
        conexion.close()
        
        return jsonify({
            "exito": True,
            "mensaje": f"¡Misión completada! Ganaste {mision['puntos_recompensa']} puntos",
            "puntos_ganados": mision['puntos_recompensa']
        })
        
    except Error as e:
        print(f"Error al completar misión: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/obtener-misiones-completadas/<int:usuario_id>")
def obtener_misiones_completadas(usuario_id):
    """Obtiene las misiones completadas por el usuario"""
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT mc.mision_id, mc.fecha_completada, m.titulo 
            FROM misiones_completadas mc
            JOIN misiones m ON mc.mision_id = m.id
            WHERE mc.usuario_id = %s
            ORDER BY mc.fecha_completada DESC
        """, (usuario_id,))
        
        misiones = []
        for fila in cursor.fetchall():
            misiones.append({
                "mision_id": fila['mision_id'],
                "titulo": fila['titulo'],
                "fecha": fila['fecha_completada'].strftime('%Y-%m-%d %H:%M:%S') if fila['fecha_completada'] else None
            })
        
        return jsonify({"misiones_completadas": misiones})
        
    finally:
        conexion.close()

@aplicacion.route("/api/recompensas")
def obtener_recompensas():
    """Obtiene todas las recompensas disponibles"""
    try:
        usuario_id = request.args.get('usuario_id')
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Obtener recompensas activas
        cursor.execute("SELECT * FROM recompensas WHERE activa = 1")
        recompensas = cursor.fetchall()
        
        # Obtener puntos disponibles del usuario
        puntos_disponibles = 0
        if usuario_id:
            cursor.execute("SELECT puntos_disponibles FROM puntos_usuario WHERE usuario_id = %s", (usuario_id,))
            resultado = cursor.fetchone()
            if resultado:
                puntos_disponibles = resultado['puntos_disponibles']
        
        conexion.close()
        return jsonify({
            "exito": True,
            "recompensas": recompensas,
            "puntos_disponibles": puntos_disponibles
        })
        
    except Error as e:
        print(f"Error al obtener recompensas: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/reclamar-recompensa", methods=["POST"])
def reclamar_recompensa():
    """Reclama una recompensa gastando puntos del usuario"""
    try:
        datos = request.json
        usuario_id = datos.get('usuario_id')
        recompensa_id = datos.get('recompensa_id')
        
        if not usuario_id or not recompensa_id:
            return jsonify({"exito": False, "mensaje": "Datos incompletos"}), 400
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        # Obtener información de la recompensa
        cursor.execute("SELECT * FROM recompensas WHERE id = %s", (recompensa_id,))
        recompensa = cursor.fetchone()
        
        if not recompensa:
            conexion.close()
            return jsonify({"exito": False, "mensaje": "Recompensa no encontrada"}), 404
        
        # Verificar puntos disponibles
        cursor.execute("SELECT puntos_disponibles FROM puntos_usuario WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        
        if not resultado or resultado['puntos_disponibles'] < recompensa['costo_puntos']:
            conexion.close()
            return jsonify({"exito": False, "mensaje": "Puntos insuficientes"}), 400
        
        # Verificar si ya reclamó esta recompensa
        cursor.execute("""
            SELECT id FROM recompensas_reclamadas 
            WHERE usuario_id = %s AND recompensa_id = %s
        """, (usuario_id, recompensa_id))
        
        if cursor.fetchone():
            conexion.close()
            return jsonify({"exito": False, "mensaje": "Ya reclamaste esta recompensa"}), 400
        
        # Registrar recompensa reclamada
        cursor.execute("""
            INSERT INTO recompensas_reclamadas (usuario_id, recompensa_id, puntos_gastados)
            VALUES (%s, %s, %s)
        """, (usuario_id, recompensa_id, recompensa['costo_puntos']))
        
        # Actualizar puntos del usuario
        cursor.execute("""
            UPDATE puntos_usuario 
            SET puntos_gastados = puntos_gastados + %s,
                puntos_disponibles = puntos_disponibles - %s
            WHERE usuario_id = %s
        """, (recompensa['costo_puntos'], recompensa['costo_puntos'], usuario_id))
        
        # Registrar en historial
        cursor.execute("""
            INSERT INTO historial_actividades (usuario_id, tipo_actividad, descripcion, puntos_cambio)
            VALUES (%s, 'Recompensa Reclamada', %s, %s)
        """, (usuario_id, recompensa['titulo'], -recompensa['costo_puntos']))
        
        conexion.commit()
        conexion.close()
        
        return jsonify({
            "exito": True,
            "mensaje": f"¡Recompensa reclamada! Gastaste {recompensa['costo_puntos']} puntos"
        })
        
    except Error as e:
        print(f"Error al reclamar recompensa: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

@aplicacion.route("/api/obtener-recompensas-usuario/<int:usuario_id>")
def obtener_recompensas_usuario(usuario_id):
    """Obtiene las recompensas reclamadas por el usuario"""
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT r.titulo, r.descripcion, r.icono, 
                   rc.fecha_reclamada, rc.puntos_gastados
            FROM recompensas_reclamadas rc
            JOIN recompensas r ON rc.recompensa_id = r.id
            WHERE rc.usuario_id = %s
            ORDER BY rc.fecha_reclamada DESC
        """, (usuario_id,))
        
        recompensas = []
        for fila in cursor.fetchall():
            recompensas.append({
                "titulo": fila['titulo'],
                "descripcion": fila['descripcion'],
                "icono": fila['icono'],
                "fecha": fila['fecha_reclamada'].strftime('%Y-%m-%d %H:%M:%S') if fila['fecha_reclamada'] else None,
                "puntos": fila['puntos_gastados']
            })
        
        return jsonify({"recompensas": recompensas})
        
    finally:
        conexion.close()

@aplicacion.route("/api/guardar-resultado-juego", methods=["POST"])
def guardar_resultado_juego():
    """Guarda el resultado de un juego"""
    datos = request.json
    usuario_id = datos.get('usuario_id')
    nombre_juego = datos.get('nombre_juego')
    puntuacion = datos.get('puntuacion')
    tiempo_jugado = datos.get('tiempo_jugado', 0)
    
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO juegos_jugados 
            (usuario_id, nombre_juego, puntuacion, tiempo_jugado)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, nombre_juego, puntuacion, tiempo_jugado))
        
        conexion.commit()
        return jsonify({"exito": True, "mensaje": "Resultado guardado"})
        
    except Error as e:
        conexion.rollback()
        return jsonify({"exito": False, "mensaje": f"Error: {str(e)}"})
    finally:
        conexion.close()

@aplicacion.route("/api/obtener-historial-juegos/<int:usuario_id>")
def obtener_historial_juegos(usuario_id):
    """Obtiene el historial de juegos del usuario"""
    conexion = obtener_conexion_bd()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT nombre_juego, puntuacion, tiempo_jugado, fecha_juego
            FROM juegos_jugados
            WHERE usuario_id = %s
            ORDER BY fecha_juego DESC
            LIMIT 20
        """, (usuario_id,))
        
        juegos = []
        for fila in cursor.fetchall():
            juegos.append({
                "nombre": fila['nombre_juego'],
                "puntuacion": fila['puntuacion'],
                "tiempo": fila['tiempo_jugado'],
                "fecha": fila['fecha_juego'].strftime('%Y-%m-%d %H:%M:%S') if fila['fecha_juego'] else None
            })
        
        return jsonify({"historial": juegos})
        
    finally:
        conexion.close()

@aplicacion.route("/api/historial")
def obtener_historial():
    """Obtiene el historial de actividades del usuario"""
    try:
        usuario_id = request.args.get('usuario_id')
        
        if not usuario_id:
            return jsonify({"exito": False, "mensaje": "ID de usuario requerido"}), 400
        
        conexion = obtener_conexion_bd()
        if not conexion:
            return jsonify({"exito": False, "mensaje": "Error de conexión"}), 500
            
        cursor = conexion.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM historial_actividades 
            WHERE usuario_id = %s 
            ORDER BY fecha_actividad DESC
        """, (usuario_id,))
        
        historial = cursor.fetchall()
        
        # Convertir datetime a string para JSON
        for actividad in historial:
            if actividad.get('fecha_actividad'):
                actividad['fecha_actividad'] = actividad['fecha_actividad'].strftime('%Y-%m-%d %H:%M:%S')
        
        conexion.close()
        return jsonify({"exito": True, "historial": historial})
        
    except Error as e:
        print(f"Error al obtener historial: {e}")
        return jsonify({"exito": False, "mensaje": str(e)}), 500

if __name__ == "__main__":
    aplicacion.run(debug=True, host='0.0.0.0', port=5000)
