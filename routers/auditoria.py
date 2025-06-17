from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import Auditoria, Usuario
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuditoriaRequest(BaseModel):
    accion: str
    usuario_id: int

@router.post("/auditoria")
def registrar_accion(data: AuditoriaRequest, request: Request, db: Session = Depends(get_db)):
    ip_cliente = request.client.host

    # Obtener nombre del usuario
    usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
    if not usuario:
        return {"error": "Usuario no encontrado"}

    nueva = Auditoria(
        accion=data.accion,
        usuario_id=data.usuario_id,
        fecha=datetime.now(),
        ip_cliente=ip_cliente
    )
    db.add(nueva)
    db.commit()
    return {
        "message": "Acción registrada correctamente",
        "usuario": usuario.nombre  # 👈 enviamos el nombre en la respuesta
    }
