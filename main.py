from fastapi import FastAPI , HTTPException , Depends
from pydantic import BaseModel, BaseModelimport 
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

#Configuracion de la base de datos
db_config = {
    'user' : 'QUtkEmySgUdyWt7.root',
    'password': 'WRb7a5VQInqeAuK3',
    'host' : 'gateway01.us-east-1.prod.aws.tidbcloud.com',
    'port' : 4000,
    'database': 'test'
}

#Modelo de datos para el login

class Loginrequest(BaseModel):
    email: str
    password : str

#Inicializar FastApi

app = FastAPI()

#Funcion para obtener la conexion a la base de datos

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return Connection

#Ruta para el login
@app.post("/login")
def login(login_request: LoginRequest):
    Connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM loguin WHERE email = %s AND PASSWORD = %s"
    cursor.execute(query, (login_request.email, login_request.password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user:
        return {"message": "Login successful" , "user": user}
    else:
        raise HTTPException(status_code=401 , detail="Invalid credentials" )  

#Ruta de prueba
@app.get("/")
def read_root():
    return{"message": "Welcome to the FastApi TiDB Gateway"}

#Ejecutar la aplicacion
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
