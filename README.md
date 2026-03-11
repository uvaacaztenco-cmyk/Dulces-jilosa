# Sistema POS Dulces Jilosa

Sistema de punto de venta desarrollado con FastAPI para la gestión de ventas de dulces funcionales.

## Tecnologías

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

## Funcionalidades

- Autenticación de usuarios
- Roles (ADMIN / CAJERO)
- Registro de ventas
- Gestión de productos
- Sincronización de ventas

## Ejecutar proyecto

Instalar dependencias:

pip install -r requirements.txt

Ejecutar servidor:

uvicorn app.main:app --reload

Abrir documentación:

http://127.0.0.1:8000/docs
