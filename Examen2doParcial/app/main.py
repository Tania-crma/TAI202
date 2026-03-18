#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Instancia del servidor
app = FastAPI()

#Seguridad HTTP BASIC
securiy = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(securiy)):
    usuario_correcto = secrets.compare_digest(credenciales.username, "admin")
    contrasena_correcta = secrets.compare_digest(credenciales.password, "rest123")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credenciales.username

#Endspoints
#Crear reservas

class reserva(BaseModel):
    "Modelo de entrada para crear una reservas"

    nombre: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Nombre del cliente (6 caracterestes minimo)"
    )

    fecha: str (date) = Field(

        ...,
    )

    invitados: int = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Cantidad de personas invitadas"
    )
    
#Listar reserva

@app.get(
    "/v1/reserva/",
    tags=["reserva"],
    summary="Listar todas las reservas"
)
    async def cancelar(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    async def listar_reservas(): "Devuelve la lista de reservas"
    return {
        "total_reservas": len(reservas),
        "reservas": reservas,
        "status": 200
    }

#Consultar por ID

@app.get(
    "/v1/reserva/buscar/",
    tags=["Reserva"],
    summary="Buscar una reserva por ID"
)
async def buscar_reserva_por_ID(id: int):
    "Busca reservas por el ID indicado"

    if not id or len(id ()) < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'ID' debe ser mayor a 0"
        )

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron reservas que contengan '{id}'"
        )

    return {
        "Reservas": resultados,
        "status": 200
    }

#Confirmar reserva



#Cancelar reserva

@app.delete("/v1/Cancelar/{id}", tags=['HTTP CRUD'])
async def cancelar(id: int):
async def cancelar(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for index, usr in enumerate(reserva):
        if usr["id"] == id:
            eliminado = reserva.pop(index)
            return {
                "mensaje": "Rerserva eliminada",
                "mensaje": f"Reserva eliminada por {usuarioAuth}",
                "reserva": eliminado,
                "status": "200"
            }
    
