from database import engine
from models import Base

# ⚠️ ¡Esto elimina todas las tablas y las vuelve a crear!
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Tablas eliminadas y recreadas correctamente.")
