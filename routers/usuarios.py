from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo de entrada para login
class LoginRequest(BaseModel):
    email: str
    api_key: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        Usuario.email == data.email,
        Usuario.api_key == data.api_key
    ).first()
    
    if user:
        return {"success": True, "usuario_id": user.id}
    
    return {"success": False, "message": "Credenciales incorrectas"}
