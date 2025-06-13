from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # ✅ ESTA LÍNEA ES LA CLAVE

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    email = Column(String(100), unique=True)
    api_key = Column(String(100))
    google_id = Column(String(100))
    
    # Relación con auditorías
    auditorias = relationship("Auditoria", back_populates="usuario")

class Auditoria(Base):
    __tablename__ = "auditoria"
    id = Column(Integer, primary_key=True, index=True)
    accion = Column(String(100))
    fecha = Column(DateTime)
    ip_cliente = Column(String(50))  # 🆕 nuevo campo para IP
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="auditorias")

