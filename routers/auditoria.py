from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Auditoria
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auditoria")
def registrar_accion(accion: str, usuario_id: int, db: Session = Depends(get_db)):
    nueva = Auditoria(accion=accion, usuario_id=usuario_id, fecha=datetime.now())
    db.add(nueva)
    db.commit()
    return {"message": "Acción registrada correctamente"}
