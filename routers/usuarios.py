from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(email: str, api_key: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email, Usuario.api_key == api_key).first()
    if user:
        return {"success": True, "usuario_id": user.id}
    return {"success": False, "message": "Credenciales incorrectas"}
