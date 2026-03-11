from app.core.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password

db = SessionLocal()

admin = User(
    username="admin",
    password_hash=hash_password("1234"),
    role="ADMIN"
)

db.add(admin)
db.commit()

print("ADMIN creado correctamente")