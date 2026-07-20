import mysql.connector
from mysql.connector import Error

def gestionar_base_datos():
    try:
        # Conexion local
        conexion = mysql.connector.connect(
            host='127.0.0.1',
            user='root',       
            password='',       
            database='floreria' 
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            print("Conectado")

            # Crear tabla usuarios
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

            # Crear tabla servicios enlazada a usuarios
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
            print("Tablas listas\n")

        while True:

            # --- Menu de Inicio de 2 Opciones ---
            print("--- MENU PRINCIPAL ---")
            print("1. Registrar nuevo usuario y flor")
            print("2. Borrar usuario por ID")
            print("3. actualizar usuario por ID")
            print("4. salir")
            opcion = input("Selecciona una opcion (1, 2, 3 o 4): ")

            if opcion == "1":
                # --- Opcion Registro ---
                print("\n--- Registro de Usuario ---")
                nombre_input = input("Introduce el nombre de usuario: ")
                email_input = input("Introduce el email: ")
                password_input = input("Introduce la contrasenia: ")

                insertar_usuario = "INSERT INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)"
                cursor.execute(insertar_usuario, (nombre_input, email_input, password_input))
                id_usuario_generado = cursor.lastrowid

                print("\n--- Registro de Flor ---")
                nombre_flor_input = input("Introduce el nombre de la flor: ")
                descripcion_input = input("Introduce la descripcion: ")
                precio_input = float(input("Introduce el precio: "))

                insertar_flor = "INSERT INTO servicios (nombre_flor, description, precio, comprador) VALUES (%s, %s, %s, %s)"
                datos_flor = (nombre_flor_input, descripcion_input, precio_input, id_usuario_generado)
                cursor.execute(insertar_flor, datos_flor)
                
                conexion.commit()
                print("Datos guardados con exito")

            elif opcion == "2":
                # --- Opcion Borrar ---
                print("\n--- Borrar Usuario de la Base de Datos ---")
                id_usuario_borrar = int(input("Introduce el ID del usuario que deseas eliminar por completo: "))
                
                # Borramos los servicios asociados a ese comprador
                sql_borrar_servicios = "DELETE FROM servicios WHERE comprador = %s"
                cursor.execute(sql_borrar_servicios, (id_usuario_borrar,))
                
                # Eliminamos al usuario de la tabla usuarios
                sql_borrar_usuario = "DELETE FROM usuarios WHERE id_usuarios = %s"
                cursor.execute(sql_borrar_usuario, (id_usuario_borrar,))
                
                conexion.commit()
                print(f"Usuario con ID {id_usuario_borrar} y sus servicios han sido eliminados")

            elif opcion == "3":
                # --- Opcion Actualizar ---
                print("\n--- Actualizar Usuario ---")
                id_usuario_actualizar = int(input("Introduce el ID del usuario que deseas actualizar: "))
                
                # Verificamos si el usuario existe
                cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (id_usuario_actualizar,))
                usuario_existente = cursor.fetchone()
                
                if usuario_existente:
                    nuevo_nombre = input("Introduce el nuevo nombre de usuario: ")
                    nuevo_email = input("Introduce el nuevo email: ")
                    nueva_password = input("Introduce la nueva contrasenia: ")
                    
                    sql_actualizar_usuario = """
                    UPDATE usuarios 
                    SET nombre_usuario = %s, email = %s, password = %s 
                    WHERE id_usuarios = %s
                    """
                    cursor.execute(sql_actualizar_usuario, (nuevo_nombre, nuevo_email, nueva_password, id_usuario_actualizar))
                    conexion.commit()
                    print(f"Usuario con ID {id_usuario_actualizar} ha sido actualizado")
                else:
                    print(f"No se encontró un usuario con ID {id_usuario_actualizar}")
            
            elif opcion == "4":
                print("Saliendo del programa")
                break           
            else:
                print("Opcion no valida")

            # --- Consulta final (Excluyendo id_servicio) ---
            consulta_relacionada = """
            SELECT s.nombre_flor, s.description, s.precio, u.nombre_usuario 
            FROM servicios s
            INNER JOIN usuarios u ON s.comprador = u.id_usuarios
            """
            cursor.execute(consulta_relacionada)
            filas = cursor.fetchall()
            
            print("\n--- Lista de Servicios Vendidos Actualizada ---")
            if not filas:
                print("No hay servicios o usuarios registrados en este momento")
            for fila in filas:
                print(f"Flor: {fila[0]} | Info: {fila[1]} | Precio: ${fila[2]} | Cliente: {fila[3]}")

    except Error as e:
        print(f"Fallo: {e}")
    except ValueError:
        print("Error: Introdujiste un formato de numero incorrecto")
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("\nConexion cerrada")

gestionar_base_datos()