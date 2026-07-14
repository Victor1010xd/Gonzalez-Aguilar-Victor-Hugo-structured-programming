import mysql.connector
from mysql.connector import Error

def gestionar_base_datos():
    try:
        # Conexión local a la base de datos
        conexion = mysql.connector.connect(
            host='127.0.0.1',
            user='root',       
            password='',       
            database='floreria' 
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            print("¡Conectado con éxito!")

            # Crear tabla usuarios si no existe
            tabla_usuarios_sql = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuarios INT(11) NOT NULL AUTO_INCREMENT,
                nombre_usuario VARCHAR(50) DEFAULT NULL,
                email VARCHAR(100) DEFAULT NULL,
                password VARCHAR(255) DEFAULT NULL,
                fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id_usuarios)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            """
            cursor.execute(tabla_usuarios_sql)

            # Crear tabla servicios enlazada a usuarios por el id del comprador
            tabla_servicios_sql = """
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INT(11) NOT NULL AUTO_INCREMENT,
                nombre_flor VARCHAR(100) NOT NULL,
                description TEXT DEFAULT NULL,
                precio DECIMAL(10,2) NOT NULL,
                comprador INT(11) DEFAULT NULL,
                PRIMARY KEY (id_servicio),
                FOREIGN KEY (comprador) REFERENCES usuarios(id_usuarios) 
                    ON DELETE SET NULL 
                    ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
            """
            cursor.execute(tabla_servicios_sql)
            print("Tablas listas y relacionadas.\n")

            # --- Prueba de inserción ---
            
            # 1. Metemos un usuario de prueba
            insertar_usuario = "INSERT INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insertar_usuario, ("Carlos Gómez", "carlos@email.com", "secure123"))
            
            # Agarramos el ID del usuario que se acaba de crear
            id_usuario_generado = cursor.lastrowid

            # 2. Metemos la flor vinculada a ese usuario
            insertar_flor = "INSERT INTO servicios (nombre_flor, description, precio, comprador) VALUES (%s, %s, %s, %s)"
            datos_flor = ("Rosas Rojas", "Ramo de 12 rosas", 250.50, id_usuario_generado)
            cursor.execute(insertar_flor, datos_flor)
            
            conexion.commit() # Guardamos los cambios
            print("Datos de prueba guardados.")

            # --- Consulta final (Sin id_servicio) ---
            consulta_relacionada = """
            SELECT s.nombre_flor, s.description, s.precio, u.nombre_usuario 
            FROM servicios s
            INNER JOIN usuarios u ON s.comprador = u.id_usuarios
            """
            cursor.execute(consulta_relacionada)
            filas = cursor.fetchall()
            
            print("\n--- Lista de Servicios Vendidos ---")
            for fila in filas:
                # Muestra: Flor | Descripción | Precio | Comprador
                print(f"Flor: {fila[0]} | Info: {fila[1]} | Precio: ${fila[2]} | Cliente: {fila[3]}")

    except Error as e:
        print(f"Hubo un fallo: {e}")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("\nConexión cerrada de compas.")

gestionar_base_datos()