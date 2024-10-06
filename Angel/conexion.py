import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            user='',
            password='',
            host='',
            database='',
            port=''
        )
        print("Connected to the database successfully")
        return conexion
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")

