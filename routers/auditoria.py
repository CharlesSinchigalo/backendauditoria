from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import Auditoria

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auditoria")
def registrar_accion(
    accion: str,
    usuario_id: int,
    request: Request,  # 🆕 para acceder a la IP
    db: Session = Depends(get_db)
):
    ip_cliente = request.client.host
    nueva = Auditoria(
        accion=accion,
        usuario_id=usuario_id,
        fecha=datetime.now(),
        ip_cliente=ip_cliente  # 🆕 IP registrada
    )
    db.add(nueva)
    db.commit()
    return {"message": "Acción registrada correctamente"}

