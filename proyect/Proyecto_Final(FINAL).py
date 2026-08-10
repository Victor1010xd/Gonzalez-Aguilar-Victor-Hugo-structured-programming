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
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuarios INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50),
                email VARCHAR(100),
                password VARCHAR(255),
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # Crear tabla servicios enlazada a usuarios
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicios (
                id_servicio INT AUTO_INCREMENT PRIMARY KEY,
                nombre_flor VARCHAR(100) NOT NULL,
                description TEXT,
                precio DECIMAL(10,2) NOT NULL,
                comprador INT,
                FOREIGN KEY (comprador) REFERENCES usuarios(id_usuarios) 
                    ON DELETE SET NULL ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            print("Tablas listas\n")

        while True:
            print("--- MENU PRINCIPAL ---")
            print("1. Registrar nuevo usuario y flor")
            print("2. Borrar usuario por ID")
            print("3. Actualizar usuario y/o flor por ID")
            print("4. Mostrar todos los usuarios y sus flores")
            print("5. Salir")
            opcion = input("Selecciona una opcion (1-5): ")

            if opcion == "1":
                # --- Registro ---
                print("\n--- Registro de Usuario ---")
                nombre_input = input("Introduce el nombre de usuario: ")

                while True:
                    email_input = input("Introduce el email: ")
                    if validar_email(email_input):
                        break
                    else:
                        print("❌ Correo inválido. Ejemplo válido: ejemplo@gmail.com")

                password_input = input("Introduce la contrasenia: ")

                cursor.execute("INSERT INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)",
                               (nombre_input, email_input, password_input))
                id_usuario_generado = cursor.lastrowid
                print(f"✅ Usuario registrado con ID: {id_usuario_generado}")

                print("\n--- Registro de Flor ---")
                nombre_flor_input = input("Introduce el nombre de la flor: ")
                descripcion_input = input("Introduce la descripcion: ")
                precio_input = float(input("Introduce el precio: "))

                cursor.execute("INSERT INTO servicios (nombre_flor, description, precio, comprador) VALUES (%s, %s, %s, %s)",
                               (nombre_flor_input, descripcion_input, precio_input, id_usuario_generado))
                conexion.commit()
                print("Datos guardados con exito")

            elif opcion == "2":
                # --- Borrar con confirmación ---
                print("\n--- Borrar Usuario ---")
                id_usuario_borrar = int(input("Introduce el ID del usuario: "))

                cursor.execute("SELECT nombre_usuario, email FROM usuarios WHERE id_usuarios = %s", (id_usuario_borrar,))
                usuario = cursor.fetchone()

                if usuario:
                    print(f"Usuario encontrado: ID {id_usuario_borrar}, Nombre: {usuario[0]}, Email: {usuario[1]}")
                    confirmacion = input("¿Seguro que deseas eliminarlo? (si/no): ").lower()

                    if confirmacion == "si":
                        cursor.execute("DELETE FROM servicios WHERE comprador = %s", (id_usuario_borrar,))
                        cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id_usuario_borrar,))
                        conexion.commit()
                        print(f"✅ Usuario con ID {id_usuario_borrar} eliminado junto con sus servicios")
                    else:
                        print("❌ Eliminación cancelada. Volviendo al menú principal...")
                else:
                    print("❌ Usuario no encontrado")

            elif opcion == "3":
                # --- Submenú de Actualización ---
                print("\n--- Actualizar Usuario y/o Flor ---")
                id_usuario_actualizar = int(input("Introduce el ID del usuario: "))
                
                cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (id_usuario_actualizar,))
                usuario_existente = cursor.fetchone()
                
                if usuario_existente:
                    while True:
                        print("\n--- SUBMENÚ ACTUALIZAR ---")
                        print("1. Actualizar nombre de usuario")
                        print("2. Actualizar email")
                        print("3. Actualizar contraseña")
                        print("4. Actualizar nombre de flor")
                        print("5. Actualizar descripción de flor")
                        print("6. Actualizar precio de flor")
                        print("7. Volver al menú principal")
                        sub_opcion = input("Selecciona una opción (1-7): ")

                        if sub_opcion == "1":
                            nuevo_nombre = input("Nuevo nombre: ")
                            cursor.execute("UPDATE usuarios SET nombre_usuario = %s WHERE id_usuarios = %s",
                                           (nuevo_nombre, id_usuario_actualizar))
                            conexion.commit()
                            print("✅ Nombre actualizado")

                        elif sub_opcion == "2":
                            while True:
                                nuevo_email = input("Nuevo email: ")
                                if validar_email(nuevo_email):
                                    break
                                else:
                                    print("❌ Correo inválido. Ejemplo válido: ejemplo@gmail.com")
                            cursor.execute("UPDATE usuarios SET email = %s WHERE id_usuarios = %s",
                                           (nuevo_email, id_usuario_actualizar))
                            conexion.commit()
                            print("✅ Email actualizado")

                        elif sub_opcion == "3":
                            nueva_password = input("Nueva contraseña: ")
                            cursor.execute("UPDATE usuarios SET password = %s WHERE id_usuarios = %s",
                                           (nueva_password, id_usuario_actualizar))
                            conexion.commit()
                            print("✅ Contraseña actualizada")

                        elif sub_opcion == "4":
                            cursor.execute("SELECT * FROM servicios WHERE comprador = %s", (id_usuario_actualizar,))
                            servicios_existentes = cursor.fetchall()
                            if servicios_existentes:
                                for servicio in servicios_existentes:
                                    print(f"Flor con ID {servicio[0]} (actual: {servicio[1]})")
                                    nuevo_nombre_flor = input("Nuevo nombre de la flor: ")
                                    cursor.execute("UPDATE servicios SET nombre_flor = %s WHERE id_servicio = %s",
                                                   (nuevo_nombre_flor, servicio[0]))
                                conexion.commit()
                                print("✅ Nombre de flor actualizado")
                            else:
                                print("❌ No hay flores asociadas a este usuario")

                        elif sub_opcion == "5":
                            cursor.execute("SELECT * FROM servicios WHERE comprador = %s", (id_usuario_actualizar,))
                            servicios_existentes = cursor.fetchall()
                            if servicios_existentes:
                                for servicio in servicios_existentes:
                                    print(f"Flor con ID {servicio[0]} (actual descripción: {servicio[2]})")
                                    nueva_descripcion = input("Nueva descripción: ")
                                    cursor.execute("UPDATE servicios SET description = %s WHERE id_servicio = %s",
                                                   (nueva_descripcion, servicio[0]))
                                conexion.commit()
                                print("✅ Descripción de flor actualizada")
                            else:
                                print("❌ No hay flores asociadas a este usuario")

                        elif sub_opcion == "6":
                            cursor.execute("SELECT * FROM servicios WHERE comprador = %s", (id_usuario_actualizar,))
                            servicios_existentes = cursor.fetchall()
                            if servicios_existentes:
                                for servicio in servicios_existentes:
                                    print(f"Flor con ID {servicio[0]} (actual precio: ${servicio[3]})")
                                    nuevo_precio = float(input("Nuevo precio: "))
                                    cursor.execute("UPDATE servicios SET precio = %s WHERE id_servicio = %s",
                                                   (nuevo_precio, servicio[0]))
                                conexion.commit()
                                print("✅ Precio de flor actualizado")
                            else:
                                print("❌ No hay flores asociadas a este usuario")

                        elif sub_opcion == "7":
                            print("Volviendo al menú principal...")
                            break
                        else:
                            print("❌ Opción inválida")
                else:
                    print("❌ Usuario no encontrado")
            elif opcion == "4":
                # --- Mostrar todos los usuarios con sus flores ---
                print("\n--- Lista de Usuarios y sus Flores ---")
                consulta = """
                SELECT u.id_usuarios, u.nombre_usuario, u.email, u.fecha_registro,
                       s.id_servicio, s.nombre_flor, s.description, s.precio
                FROM usuarios u
                LEFT JOIN servicios s ON u.id_usuarios = s.comprador
                ORDER BY u.id_usuarios, s.id_servicio
                """
                cursor.execute(consulta)
                registros = cursor.fetchall()

                if not registros:
                    print("No hay usuarios registrados")
                else:
                    print("{:<5} {:<15} {:<25} {:<20} {:<7} {:<15} {:<25} {:<10}".format(
                        "ID", "Nombre", "Email", "Fecha Registro", "IDFlor", "Flor", "Descripcion", "Precio"))
                    print("-" * 130)
                    for r in registros:
                        id_flor = r[4] if r[4] else "-"
                        flor = r[5] if r[5] else "Sin flor"
                        descripcion = r[6] if r[6] else "-"
                        precio = f"${r[7]}" if r[7] else "-"
                        print("{:<5} {:<15} {:<25} {:<20} {:<7} {:<15} {:<25} {:<10}".format(
                            r[0], r[1], r[2], str(r[3]), id_flor, flor, descripcion, precio))

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
