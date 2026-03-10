#Importaciones
from fastapi import FastAPI
import asyncio

#Instancia del servidor
app = FastAPI()

#Endspoints
@app.get("/")
async def holamudo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {"mensaje":"Bienvenido a FastAPI",
            "estatus":"200",
            }