from fastapi import FastAPI
from models import Base
from database import engine
from routers import usuarios, auditoria

app = FastAPI()

# Crear las tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(usuarios.router)
app.include_router(auditoria.router)
