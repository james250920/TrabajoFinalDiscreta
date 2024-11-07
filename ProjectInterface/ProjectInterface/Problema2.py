from conexion import obtener_amistades, obtener_nombres_usuarios, conectar, cerrar_conexion


# Función para recomendar amigos
def recomendar_amigos(amistades, conexion):
    # Obtener los nombres de los usuarios
    nombres_usuarios = obtener_nombres_usuarios(conexion)

    # Diccionario para almacenar las relaciones de amistad
    relaciones = {}

    # Construcción del grafo de relaciones de amistad
    for usuario1, usuario2 in amistades:
        # Obtener los nombres de los usuarios desde el diccionario
        nombre_usuario1 = nombres_usuarios.get(usuario1)
        nombre_usuario2 = nombres_usuarios.get(usuario2)

        if nombre_usuario1 and nombre_usuario2:
            if nombre_usuario1 not in relaciones:
                relaciones[nombre_usuario1] = set()
            if nombre_usuario2 not in relaciones:
                relaciones[nombre_usuario2] = set()

            # Añadir la relación de amistad en ambos sentidos
            relaciones[nombre_usuario1].add(nombre_usuario2)
            relaciones[nombre_usuario2].add(nombre_usuario1)

    # Para cada usuario, encontramos posibles recomendaciones
    for usuario, amigos in relaciones.items():
        posibles_recomendaciones = set()

        # Iterar sobre los amigos del usuario
        for amigo in amigos:
            # Obtener los amigos del amigo (exceptuando al propio usuario y sus amigos)
            if amigo in relaciones:
                amigos_del_amigo = relaciones[amigo] - {usuario} - amigos
                posibles_recomendaciones.update(amigos_del_amigo)

        # Imprimir las recomendaciones para el usuario
        print(f"Usuario: {usuario}")
        if posibles_recomendaciones:
            print(f"  Recomendados: {', '.join(posibles_recomendaciones)}")
        else:
            print("  No hay recomendaciones de amigos.")
        print()


# Función principal
def main():
    conexion = conectar()

    if conexion:
        # Obtener las amistades desde la base de datos
        amistades = obtener_amistades(conexion)

        if amistades:
            # Llamar a la función de recomendación de amigos
            recomendar_amigos(amistades, conexion)

        # Cerrar la conexión a la base de datos
        cerrar_conexion(conexion)
    else:
        print("No se pudo conectar a la base de datos")


if __name__ == "__main__":
    main()
