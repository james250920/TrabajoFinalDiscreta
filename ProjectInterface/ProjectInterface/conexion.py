import mysql.connector


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sistemas",
            database="finaldiscreta"
        )
        print("Connected to the database successfully")
        return conexion
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")
        return None


# Método para obtener las amistades
def obtener_amistades(conexion):
    try:
        with conexion.cursor() as cursor:
            # Consulta para obtener las amistades
            query = """
            SELECT u1.nombre, u2.nombre 
            FROM Amistades a
            JOIN Usuarios u1 ON a.id_usuario1 = u1.id
            JOIN Usuarios u2 ON a.id_usuario2 = u2.id
            """
            cursor.execute(query)
            amistades = cursor.fetchall()
            return amistades
    except mysql.connector.Error as err:
        print(f"Error fetching friendships: {err}")
        return None


# Método para obtener los usuarios
def obtener_usuarios(conexion):
    try:
        with conexion.cursor() as cursor:
            # Consulta para obtener todos los usuarios
            query = "SELECT * FROM Usuarios"
            cursor.execute(query)
            usuarios = cursor.fetchall()
            return usuarios
    except mysql.connector.Error as err:
        print(f"Error fetching users: {err}")
        return None


# Ejemplo de uso:
conexion = conectar()

if conexion:
    # Ver amistades en consola
    amistades = obtener_amistades(conexion)
    if amistades:
        print("Amistades:", amistades)

    # Ver usuarios en consola
    usuarios = obtener_usuarios(conexion)
    if usuarios:
        print("Usuarios:", usuarios)

    # Cerrar la conexión después de usarla
    conexion.close()
else:
    print("No se pudo establecer conexión a la base de datos")
