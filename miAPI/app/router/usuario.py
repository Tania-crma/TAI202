from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios", 
    tags=["HTTP CRUD"])

# Usuario CRUD

@router.get("/")
async def leer_usuarios():
    return {"total": len(usuarios), "usuarios": usuarios, "status": "200"}
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail="El id ya existe")

    usuarios.append(usuario.model_dump())       
    return {
        "mensaje": "Usuario creado",  
        "datos nuevos": usuario,
        "status": "200"
    }

@router.put("/")
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

@router.patch("/")
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

@router.delete("/")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "usuario": eliminado,
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400, 
                detail="El id ya existe"
                )
    usuarios.append(usuario)
    return {
        "mensaje" : "Usuario agregado",
        "Usuario" : usuario
    }
