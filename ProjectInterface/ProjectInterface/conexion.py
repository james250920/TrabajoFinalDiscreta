import mysql.connector
from mysql.connector import Error


# Conectar a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sistemas",
            database="fdiscreta"
        )

        if conexion.is_connected():
            print("Connected to the database successfully")
            return conexion

    except Error as err:
        print(f"Failed to connect to the database: {err}")
        return None


# Cerrar la conexión a la base de datos
def cerrar_conexion(conexion):
    if conexion and conexion.is_connected():
        conexion.close()
        print("Connection closed successfully")


# Obtener las amistades desde la base de datos
def obtener_amistades(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario1, id_usuario2 FROM amistades")
        amistades = cursor.fetchall()
        return amistades
    except Error as err:
        print(f"Error fetching amistades: {err}")
        return []
    finally:
        cursor.close()


# Función para obtener los nombres de los usuarios desde la base de datos
def obtener_nombres_usuarios(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM Usuarios")
        usuarios = cursor.fetchall()
        # Crear un diccionario con id como clave y nombre como valor
        return {usuario[0]: usuario[1] for usuario in usuarios}
    except Error as err:
        print(f"Error fetching user names: {err}")
        return {}
    finally:
        cursor.close()
