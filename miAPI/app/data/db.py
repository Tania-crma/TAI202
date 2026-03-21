from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

# Definir la URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )

# Creamos el motor de la conexión
engine = create_engine(DATABASE_URL)

# Preparamos el gestionador de sesiones
sessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

# Base declativa del modelo
Base = declarative_base()

# Obtener la sesiones de cada petición
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()