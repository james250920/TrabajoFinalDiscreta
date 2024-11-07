#coneccion con mysql
import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sistemas",
            database="MarketBasketAnalysis"
        )
        print("Connected to the database successfully")
        return conexion
    except mysql.connector.Error as err:
        print(f"Failed to connect to the database: {err}")
        return None