from pydantic import BaseModel

# 🔹 Crear usuario
class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # ADMIN, CAJERO, INVENTARIO


# 🔹 Login
class UserLogin(BaseModel):
    username: str
    password: str


# 🔹 Respuesta pública (sin password)
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True