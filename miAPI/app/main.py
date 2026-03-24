from fastapi import FastAPI
from app.router import usuario, misc
from app.data.db import engine
from app.data import usuarios as usuarioDB

usuarioDB.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi primer API",
    description="Tania Asunción Cruz Márquez",
    version="1.0"
)

app.include_router(usuario.router)
app.include_router(misc.misc)