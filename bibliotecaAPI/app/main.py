from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date, datetime

app = FastAPI(
    title="Biblioteca Digital API",
    description="API REST para gestión de libros y préstamos",
    version="1.0"
)

libros: list[dict] = []       
prestamos: list[dict] = []      
prestamo_id_counter = 1         

class LibroIn(BaseModel):
    "Modelo de entrada para registrar un libro"

    id: int = Field(..., gt=0, description="ID único del libro (entero positivo)")

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del libro (entre 2 y 100 caracteres)"
    )

    autor: str = Field(
        ...,
        min_length=3,
        max_length=80,
        description="Nombre del autor"
    )

    anio: int = Field(
        ...,
        description="Año de publicación (mayor a 1450 y <= año actual)"
    )

    paginas: int = Field(
        ...,
        gt=1,
        description="Número de páginas (entero positivo mayor a 1)"
    )

    estado: str = Field(
        default="disponible",
        description="Estado del libro: 'disponible' o 'prestado'"
    )

    @field_validator("anio")
    @classmethod
    def validar_anio(cls, v):
        anio_actual = datetime.now().year
        if v <= 1450:
            raise ValueError("El año debe ser mayor a 1450")
        if v > anio_actual:
            raise ValueError(f"El año no puede ser mayor al año actual ({anio_actual})")
        return v

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v):
        if v not in ["disponible", "prestado"]:
            raise ValueError("El estado debe ser 'disponible' o 'prestado'")
        return v

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("El nombre del libro debe tener al menos 2 caracteres")
        return v


class UsuarioPrestamoIn(BaseModel):
    "Modelo de datos del usuario para registrar un préstamo"

    nombre: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="Nombre completo del usuario"
    )

    correo: EmailStr = Field(
        ...,
        description="Correo electrónico válido del usuario"
    )

@app.get("/", tags=["General"])
async def raiz():
    return {
        "mensaje": "Bienvenido a la API de Biblioteca Digital",
        "version": "1.0",
        "documentacion": "/docs"
    }

@app.post(
    "/v1/libros/",
    tags=["Libros"],
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo libro"
)
async def registrar_libro(libro: LibroIn):
    "Registra un libro nuevo en la biblioteca"
   
    for lb in libros:
        if lb["id"] == libro.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un libro con el id {libro.id}"
            )

    nuevo = libro.model_dump()
    nuevo["estado"] = "disponible"  
    libros.append(nuevo)

    return {
        "mensaje": "Libro registrado correctamente",
        "libro": nuevo,
        "status": 201
    }

@app.get(
    "/v1/libros/",
    tags=["Libros"],
    summary="Listar todos los libros"
)
async def listar_libros():
    "Devuelve la lista completa de libros en la biblioteca"

    disponibles = [lb for lb in libros if lb["estado"] == "disponible"]
    return {
        "total_libros": len(libros),
        "total_disponibles": len(disponibles),
        "libros": libros,
        "status": 200
    }

@app.get(
    "/v1/libros/buscar/",
    tags=["Libros"],
    summary="Buscar un libro por nombre"
)
async def buscar_libro_por_nombre(nombre: str):
    "Busca libros cuyo nombre contenga el texto indicado"

    if not nombre or len(nombre.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parámetro 'nombre' debe tener al menos 2 caracteres"
        )

    resultados = [
        lb for lb in libros
        if nombre.lower() in lb["nombre"].lower()
    ]

    if not resultados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron libros que contengan '{nombre}'"
        )

    return {
        "total_encontrados": len(resultados),
        "libros": resultados,
        "status": 200
    }

@app.post(
    "/v1/prestamos/",
    tags=["Préstamos"],
    status_code=status.HTTP_201_CREATED,
    summary="Registrar el préstamo de un libro"
)
async def registrar_prestamo(libro_id: int, usuario: UsuarioPrestamoIn):
    "Registra el préstamo de un libro a un usuario"

    global prestamo_id_counter

    libro_encontrado = None
    for lb in libros:
        if lb["id"] == libro_id:
            libro_encontrado = lb
            break

    if not libro_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un libro con id {libro_id}"
        )

   
    if libro_encontrado["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El libro '{libro_encontrado['nombre']}' ya está prestado"
        )

    
    libro_encontrado["estado"] = "prestado"

   
    nuevo_prestamo = {
        "id": prestamo_id_counter,
        "libro_id": libro_id,
        "nombre_libro": libro_encontrado["nombre"],
        "usuario_nombre": usuario.nombre,
        "usuario_correo": usuario.correo,
        "fecha_prestamo": str(date.today()),
        "devuelto": False
    }
    prestamos.append(nuevo_prestamo)
    prestamo_id_counter += 1

    return {
        "mensaje": "Préstamo registrado correctamente",
        "prestamo": nuevo_prestamo,
        "status": 201
    }

@app.patch(
    "/v1/prestamos/{prestamo_id}/devolver",
    tags=["Préstamos"],
    summary="Marcar un libro como devuelto"
)
async def devolver_libro(prestamo_id: int):
    "Marca el préstamo como devuelto y cambia el estado del libro a 'disponible'"

    prestamo_encontrado = None
    for pr in prestamos:
        if pr["id"] == prestamo_id:
            prestamo_encontrado = pr
            break

    if not prestamo_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un préstamo con id {prestamo_id}"
        )

    if prestamo_encontrado["devuelto"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El préstamo con id {prestamo_id} ya fue marcado como devuelto anteriormente"
        )

    prestamo_encontrado["devuelto"] = True
    prestamo_encontrado["fecha_devolucion"] = str(date.today())

   
    for lb in libros:
        if lb["id"] == prestamo_encontrado["libro_id"]:
            lb["estado"] = "disponible"
            break

    return {
        "mensaje": "Libro devuelto correctamente",
        "prestamo": prestamo_encontrado,
        "status": 200
    }

@app.delete(
    "/v1/prestamos/{prestamo_id}",
    tags=["Préstamos"],
    summary="Eliminar el registro de un préstamo"
)
async def eliminar_prestamo(prestamo_id: int):
    "Elimina permanentemente el registro de un préstamo"

    for index, pr in enumerate(prestamos):
        if pr["id"] == prestamo_id:
            eliminado = prestamos.pop(index)
           
            if not eliminado["devuelto"]:
                for lb in libros:
                    if lb["id"] == eliminado["libro_id"]:
                        lb["estado"] = "disponible"
                        break
            return {
                "mensaje": "Registro de préstamo eliminado correctamente",
                "prestamo_eliminado": eliminado,
                "status": 200
            }

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"El registro del préstamo con id {prestamo_id} ya no existe"
    )

@app.get(
    "/v1/prestamos/",
    tags=["Préstamos"],
    summary="Listar todos los préstamos"
)
async def listar_prestamos():
    "Devuelve todos los registros de préstamos"
    
    activos = [pr for pr in prestamos if not pr["devuelto"]]
    return {
        "total_prestamos": len(prestamos),
        "prestamos_activos": len(activos),
        "prestamos": prestamos,
        "status": 200
    }