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

class RegisterRequest(BaseModel):
    email: str
    password: str

#Modelo de datos para actualizacion
class UpdateRequest(BaseModel):
    current_email: str
    new_email: str
    new_password: str


#Inicializar FastApi
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

#Funcion para obtener la conexion a la base de datos

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return Connection

#Ruta para el login
@app.post("/login")
def login(login_request: LoginRequest):
    print(f"Received email: {login_request.email}")
    print(f"received password: {login_request.password}")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "Select * from loguin WHERE email = %s AND password = %s"
    cursor.execute(query, (login_request.email, login_request.password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return {"mesage": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=401 detail="Invalid credentials")
    

  
@app.post("/register")
def register(register_request: RegisterRequest):
    print(f"Register attempt with email: {register_request.email}")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary= True)

    #Verificar si el email ya existe
    check_query = "Select * from loguin Where email = %s"
    cursor.execute(check_query, (register_request.email))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Insertar nuevo usuario
    insert_query = "Insert Into loguin (email, password) values (%s, %s)"
    cursor.execute(insert_query, (register_request.email, register_request.password))
    connection.commit()

    #Obtener el usuario recien creado
    cursor.execute(check_query, (register_request.email,))
    new_user = cursor.fetchone()

    cursor.close()
    connection.close()

    if new_user:
        return {"message": "Registration successful" , "user": new_user}
    else:
        raise HTTPException(status_code=500, detail="Registration failed")
    


#Ruta para eliminar usuario
@app.delete("/delete_user/{emial}")
def delete_user(email: str):
    print(f"Delete attempt for email: {email}")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    #Verificar si el email existe
    check_query = "Select * from loguin Where email = %s"
    cursor.execute(check_query, (email,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    #Eliminar Usuario
    delete_query = "Delete from loguin Where email = %s"
    cursor.execute(delete_query, (email,))
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    if affected_rows > 0:
        return {"message": f"User {email} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Delete operation failed")
    
#Ruta de prueba
@app.get("/users")
def get_all_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = "Select * from loguin"
        cursor.execute(query)
        users = cursor.fetchall()
        return {"users"; users}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

#Ruta para actualizar usuarios
@app.put("/update_user")
def update_user(update_request: UpdateRequest):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        #verificar si el usuario actual existe
        check_query = "Select * from loguin Where email = %s"
        cursor.execute(check_query, (update_request.current_email,))
        existing_user = cursor.fetchone()

        if not existing_user:
            raise HTTPException(status_code=400 , detail="Usuario no encontrado")
        
        #Verificar si el nuevo email ya esta en uso
        if update_request.current_email != update_request.new_email:
            cursor.execute(check_query, (update_request.new_email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El nuevo email ya esta en uso")
            
        #Actualizar usuario
        update_query = "Update loguin Set email = %s, password=%s Where email = %s"
        cursor.execute(update_query, (
            update_request.new_email,
            update_request.new_password,
            update_request.current_email
        ))

        connection.commit()

        return {"message": "Usuario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")
    finally:
        cursor.close()
        connection.close()

#Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastApi TiBD Gateway"}

#Ejecutar la aplicacion
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)