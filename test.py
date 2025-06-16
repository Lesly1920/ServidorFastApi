import mysql.connector
import os

#Configuracion de la base de datos
db_config = {
    'user' : 'QUtkEmySgUdyWt7.root',
    'password': 'WRb7a5VQInqeAuK3',
    'host' : 'gateway01.us-east-1.prod.aws.tidbcloud.com',
    'port' : 4000,
    'database': 'test'
}

#Intentar conectarse a la base de datos
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    #Ejecutar una consulta de prueba
    cursor.execute("Select 1")
    result = cursor.fetchone()

    print("Conexion exitosa a la base de datos.Resultado de la consulta: ", result)
except mysql.connector.Error as err:
    print("Error al conectarse a la base de datos:", err)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexion cerrada.")

        