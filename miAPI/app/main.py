#Importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

#Instancia del servidor
app = FastAPI(
    title="Mi primer API",
    description="Tania Asunción Cruz Márquez",
    version="1.0"
)

#TB ficticia
usuarios = [
    {"id":1, "nombre":"Tania", "edad":22},
    {"id":2, "nombre":"David", "edad":19},
    {"id":3, "nombre":"Mario", "edad":23},
]

#Endpoints
@app.get("/")
async def holamudo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje":"Bienvenido a FastAPI", "estatus":"200"}

@app.get("/v1/parametro0b/{id}", tags=['Parametros Obligatorios'])
async def consultauno(id:int):
    return {"mensaje": "usuario encontrado", "usuario": id, "status": "200"}
    
@app.get("/v1/parametro0p/", tags=['Parametros Opcionales'])
async def consultados(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuarioK}
        return {"mensaje": "usuario no encontrado", "status": "200"}
    else:
        return {"mensaje": "No se proporcionó un id", "status": "200"}

@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {"total": len(usuarios), "usuarios": usuarios, "status": "200"}
    

@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuario(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail="El id ya existe")

    usuarios.append(usuario)          
    return {
        "mensaje": "Usuario creado",  
        "datos nuevos": usuario,
        "status": "201"
    }

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = {"id": id, **{k: v for k, v in usuario.items() if k != "id"}}
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuarios[index],
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(id: int, campos: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update({k: v for k, v in campos.items() if k != "id"})
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "usuario": usr,
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": eliminado,
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")