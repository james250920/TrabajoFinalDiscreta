from conexion import *

#conectamos a la base de datos
def conectarBD():
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT u1.nombre, GROUP_CONCAT(u2.nombre) FROM Amistades as a INNER JOIN Usuario as u1  on a.idUsuario1 = u1.id INNER JOIN Usuario as u2 on a.idUsuario2 = u2.id GROUP BY u1.nombre; ")
        usuarios = cursor.fetchall()    
        con.commit()
        con.close()
        return usuarios
    except Exception as e:
        print(f"Error al mostrar los usuarios: {e}".format(e))

#mostramos los usuarios
usuarios=conectarBD()


def mostrarUsuarios(usuarios):
    print("Listado de Usuarios:")
    for usuario in usuarios:
        print(f"Nombre: {usuario[0]}, Amigos: {usuario[1]}")

mostrarUsuarios(usuarios)
    
    

