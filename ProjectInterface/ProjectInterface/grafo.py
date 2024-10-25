import mysql.connector


def obtener_grafo():
    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sistemas",
        database="finaldiscreta"
    )

    cursor = conn.cursor()

    # Crear el diccionario (grafo) de adyacencia
    grafo = {}

    # Obtener los nombres de los usuarios
    cursor.execute("SELECT id, nombre FROM Usuarios")
    usuarios = cursor.fetchall()  # Lista de tuplas (id, nombre)

    # Inicializar el grafo
    for usuario in usuarios:
        grafo[usuario[0]] = []  # Cada usuario tendrá una lista vacía de amigos

    # Obtener las amistades
    cursor.execute("SELECT id_usuario1, id_usuario2 FROM Amistades")
    amistades = cursor.fetchall()  # Lista de tuplas (id_usuario1, id_usuario2)

    # Crear las conexiones en el grafo
    for amistad in amistades:
        id1, id2 = amistad
        grafo[id1].append(id2)
        grafo[id2].append(id1)

    cursor.close()
    conn.close()

    return grafo, usuarios
