from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import Auditoria
from pydantic import BaseModel
from sqlalchemy.orm import joinedload  # 👈 importa esto si no lo tienes


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo para recibir los datos del body
class AuditoriaRequest(BaseModel):
    accion: str
    usuario_id: int

@router.post("/auditoria")
def registrar_accion(
    data: AuditoriaRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip_cliente = request.client.host
    nueva = Auditoria(
        accion=data.accion,
        usuario_id=data.usuario_id,
        fecha=datetime.now(),
        ip_cliente=ip_cliente
    )
    db.add(nueva)
    db.commit()
    return {"message": "Acción registrada correctamente"}

@router.get("/auditoria")
def listar_auditorias(db: Session = Depends(get_db)):
    auditorias = db.query(Auditoria).options(joinedload(Auditoria.usuario)).all()
    return [
        {
            "id": a.id,
            "accion": a.accion,
            "fecha": a.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "ip_cliente": a.ip_cliente,
            "usuario": a.usuario.nombre if a.usuario else "Desconocido"
        }
        for a in auditorias
    ]
