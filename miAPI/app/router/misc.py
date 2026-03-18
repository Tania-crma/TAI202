import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

misc = APIRouter(tags=["varios"])

#Endpoints
@misc.get("/")
async def holamudo():
    return {"mensaje":"Hola mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje":"Bienvenido a FastAPI", "estatus":"200"}

@misc.get("/v1/parametro0b/{id}", tags=['Parametros Obligatorios'])
async def consultauno(id:int):
    return {"mensaje": "usuario encontrado", "usuario": id, "status": "200"}
    
@misc.get("/v1/parametro0p/", tags=['Parametros Opcionales'])
async def consultados(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": "200"}
    else:
        return {"mensaje": "No se proporcionó un id", "status": "200"} 