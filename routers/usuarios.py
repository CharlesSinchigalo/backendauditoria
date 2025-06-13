from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Usuario, Auditoria
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos de entrada
class LoginRequest(BaseModel):
    email: str
    api_key: str

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    api_key: str
    google_id: str

class UsuarioUpdate(BaseModel):
    nombre: str

# Función para registrar auditoría
def registrar_auditoria(db, usuario_id: int, accion: str, ip: str):
    registro = Auditoria(
        accion=accion,
        usuario_id=usuario_id,
        fecha=datetime.now(),
        ip_cliente=ip
    )
    db.add(registro)
    db.commit()

# Ruta: login
@router.post("/login")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(
        Usuario.email == data.email,
        Usuario.api_key == data.api_key
    ).first()

    if user:
        registrar_auditoria(db, user.id, "Inicio de sesión", request.client.host)
        return {"success": True, "usuario_id": user.id}
    
    return {"success": False, "message": "Credenciales incorrectas"}

# Ruta: crear usuario
@router.post("/usuarios")
def crear_usuario(request: Request, data: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = Usuario(
        nombre=data.nombre,
        email=data.email,
        api_key=data.api_key,
        google_id=data.google_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    registrar_auditoria(db, nuevo.id, "Usuario creado", request.client.host)
    return {"message": "Usuario creado", "usuario_id": nuevo.id}

# Ruta: actualizar usuario
@router.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.nombre = data.nombre
    db.commit()

    registrar_auditoria(db, usuario_id, "Usuario actualizado", request.client.host)
    return {"message": "Usuario actualizado"}

# Ruta: eliminar usuario
@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()

    registrar_auditoria(db, usuario_id, "Usuario eliminado", request.client.host)
    return {"message": "Usuario eliminado"}
