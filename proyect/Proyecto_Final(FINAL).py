import mysql.connector
from mysql.connector import Error
import re

# --- Función para validar email ---
def validar_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, email) is not None

def gestionar_base_datos():
    try:
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
            print("--- MENU PRINCIPAL ---")
            print("1. Registrar nuevo usuario y flor")
            print("2. Borrar usuario por ID")
            print("3. Actualizar usuario y flor por ID")
            print("4. Mostrar todos los usuarios")
            print("5. Salir")
            opcion = input("Selecciona una opcion (1-5): ")

            if opcion == "1":
                # --- Registro ---
                print("\n--- Registro de Usuario ---")
                nombre_input = input("Introduce el nombre de usuario: ")

                # Validación de correo
                while True:
                    email_input = input("Introduce el email: ")
                    if validar_email(email_input):
                        break
                    else:
                        print("❌ Correo inválido. Ejemplo válido: ejemplo@gmail.com")

                password_input = input("Introduce la contrasenia: ")

                insertar_usuario = "INSERT INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)"
                cursor.execute(insertar_usuario, (nombre_input, email_input, password_input))
                id_usuario_generado = cursor.lastrowid

                print(f"✅ Usuario registrado con ID: {id_usuario_generado}")

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
                # --- Borrar ---
                print("\n--- Borrar Usuario ---")
                id_usuario_borrar = int(input("Introduce el ID del usuario: "))
                
                cursor.execute("DELETE FROM servicios WHERE comprador = %s", (id_usuario_borrar,))
                cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id_usuario_borrar,))
                conexion.commit()
                print(f"Usuario con ID {id_usuario_borrar} eliminado junto con sus servicios")

            elif opcion == "3":
                # --- Actualizar Usuario y Flor ---
                print("\n--- Actualizar Usuario y Flor ---")
                id_usuario_actualizar = int(input("Introduce el ID del usuario: "))
                
                cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (id_usuario_actualizar,))
                usuario_existente = cursor.fetchone()
                
                if usuario_existente:
                    nuevo_nombre = input("Nuevo nombre: ")

                    # Validación de correo en actualización
                    while True:
                        nuevo_email = input("Nuevo email: ")
                        if validar_email(nuevo_email):
                            break
                        else:
                            print("❌ Correo inválido. Ejemplo válido: ejemplo@gmail.com")

                    nueva_password = input("Nueva contrasenia: ")
                    
                    sql_actualizar_usuario = """
                    UPDATE usuarios 
                    SET nombre_usuario = %s, email = %s, password = %s 
                    WHERE id_usuarios = %s
                    """
                    cursor.execute(sql_actualizar_usuario, (nuevo_nombre, nuevo_email, nueva_password, id_usuario_actualizar))

                    # --- Actualizar Flor asociada ---
                    cursor.execute("SELECT * FROM servicios WHERE comprador = %s", (id_usuario_actualizar,))
                    servicios_existentes = cursor.fetchall()

                    if servicios_existentes:
                        for servicio in servicios_existentes:
                            print(f"\nActualizando flor con ID {servicio[0]} (actual: {servicio[1]}, {servicio[2]}, ${servicio[3]})")
                            nuevo_nombre_flor = input("Nuevo nombre de la flor: ")
                            nueva_descripcion = input("Nueva descripcion: ")
                            nuevo_precio = float(input("Nuevo precio: "))

                            sql_actualizar_flor = """
                            UPDATE servicios
                            SET nombre_flor = %s, description = %s, precio = %s
                            WHERE id_servicio = %s
                            """
                            cursor.execute(sql_actualizar_flor, (nuevo_nombre_flor, nueva_descripcion, nuevo_precio, servicio[0]))

                    conexion.commit()
                    print(f"✅ Usuario con ID {id_usuario_actualizar} y sus flores han sido actualizados")
                else:
                    print("❌ Usuario no encontrado")

            elif opcion == "4":
                # --- Mostrar todos los usuarios ---
                print("\n--- Lista de Usuarios ---")
                cursor.execute("SELECT id_usuarios, nombre_usuario, email, fecha_registro FROM usuarios")
                usuarios = cursor.fetchall()
                if not usuarios:
                    print("No hay usuarios registrados")
                else:
                    print("{:<5} {:<15} {:<25} {:<20}".format("ID", "Nombre", "Email", "Fecha Registro"))
                    print("-" * 70)
                    for u in usuarios:
                        print("{:<5} {:<15} {:<25} {:<20}".format(u[0], u[1], u[2], str(u[3])))

            elif opcion == "5":
                print("Saliendo del programa")
                break
            else:
                print("Opcion no valida")

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
