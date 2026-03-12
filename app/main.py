from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
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

import app.models


app = FastAPI(title="Dulces Jilosa POS Local")


# =========================================
# CORS
# =========================================

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# CREAR TABLAS
# =========================================

Base.metadata.create_all(bind=engine)


# =========================================
# DB SESSION
# =========================================

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
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "CAJERO"]))
):
    return db.query(Product).all()


# =========================================
# CREAR PRODUCTO
# =========================================

@app.post("/productos")
def crear_producto(
    name: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):

    producto = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.add(producto)
    db.commit()
    db.refresh(producto)

    return producto


# =========================================
# ACTUALIZAR PRODUCTO
# =========================================

@app.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: int,
    name: str,
    price: float,
    stock: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):

    producto = db.query(Product).filter(Product.id == producto_id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.name = name
    producto.price = price
    producto.stock = stock

    db.commit()

    return producto


# =========================================
# ELIMINAR PRODUCTO
# =========================================

@app.delete("/productos/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):

    producto = db.query(Product).filter(Product.id == producto_id).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return {"mensaje": "Producto eliminado"}


# =========================================
# VENTAS
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
# USUARIOS
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
# SYNC LOOP
# =========================================

start_sync_loop()