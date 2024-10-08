def recomendar_amigos(u):
    relaciones = {}
    for usuario, amigos in u:
        relaciones[usuario] = set(amigos.split(', '))

    for usuario, amigos in relaciones.items():
        posibles_recomendaciones = set()
        for amigo in amigos:
            if amigo in relaciones:
                amigos_del_amigo = relaciones[amigo] - {usuario} - amigos
                posibles_recomendaciones.update(amigos_del_amigo)

        print(f"Usuario: {usuario}")
        if posibles_recomendaciones:
            print(f" Recomendados: {', '.join(posibles_recomendaciones)}")
        else:
            print("  No hay recomendaciones de amigos.")
        print()

usuarios = [
    ("Juan", "María, Pedro"),
    ("María", "Ana"),
    ("Pedro", "Ana, Luis, Carlos"),
    ("Ana", "Juan, Pedro")
]

recomendar_amigos(usuarios)
