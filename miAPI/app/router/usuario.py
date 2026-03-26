from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario, actualizar_usuario_parcial
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuarios import Usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"])


@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return {
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios,
        "status": "200"
    }


@router.get("/{id}")
async def leer_usuario(id: int, db: Session = Depends(get_db)):
    usr = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usr:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "usuario": usr,
        "status": "200"
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    nuevoU = dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
    return {
        "mensaje": "Usuario creado",
        "datos nuevos": nuevoU,
        "status": "201"
    }

@router.put("/{id}")
async def actualizar_usuario(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usr = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usr:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usr.nombre = usuarioP.nombre
    usr.edad = usuarioP.edad
    db.commit()
    db.refresh(usr)
    return {
        "mensaje": "Usuario actualizado",
        "usuario": usr,
        "status": "200"
    }


@router.patch("/{id}")
async def actualizar_usuario_parcial_endpoint(id: int, campos: actualizar_usuario_parcial, db: Session = Depends(get_db)):
    usr = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usr:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Solo actualizar campos que vienen con valor (exclude_unset ignora los no enviados)
    datos = campos.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(usr, campo, valor)
    db.commit()
    db.refresh(usr)
    return {
        "mensaje": "Usuario actualizado parcialmente",
        "usuario": usr,
        "status": "200"
    }


@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    usr = db.query(dbUsuario).filter(dbUsuario.id == id).first()
    if not usr:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usr)
    db.commit()
    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "usuario": usr,
        "status": "200"
    }
