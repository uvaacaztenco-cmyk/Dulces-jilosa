from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import engine, Base, SessionLocal
from app.services.sale_service import create_sale
from app.services.sync_service import start_sync_loop
from app.models.product import Product
from app.models.user import User
from app.schemas.sale_schema import SaleCreateSchema
from app.schemas.user_schema import UserCreate
from app.services.auth_service import (
    hash_password,
    create_access_token,
    authenticate_user
)
from app.core.security import require_roles

import app.models  # IMPORTANTE: registra todos los modelos

app = FastAPI(title="Dulces Jilosa POS Local")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)


# 🔹 Dependency para obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# PRODUCTOS
# =========================================

@app.get("/productos", summary="Obtener lista de productos")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# =========================================
# VENTAS (ADMIN Y CAJERO)
# =========================================

@app.post("/ventas", summary="Registrar venta")
def register_sale(
    data: SaleCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "CAJERO"]))
):
    try:
        sale = create_sale(
            db,
            [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in data.items
            ]
        )

        return {
            "mensaje": "Venta registrada correctamente",
            "sale_id": sale.id,
            "total": sale.total
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================================
# USUARIOS (SOLO ADMIN)
# =========================================

@app.post("/usuarios", summary="Crear usuario (Solo ADMIN)")
def crear_usuario(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):

    user_existente = db.query(User).filter(User.username == data.username).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = User(
        username=data.username,
        password_hash=hash_password(data.password),
        role=data.role
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"mensaje": "Usuario creado correctamente"}


# =========================================
# LOGIN
# =========================================

@app.post("/login", summary="Iniciar sesión")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # 🔥 AHORA EL TOKEN GUARDA TAMBIÉN EL ROL
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================
# INICIAR MOTOR DE SINCRONIZACIÓN
# =========================================

start_sync_loop()