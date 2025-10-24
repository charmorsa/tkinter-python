from fastapi import FastAPI, HTTPException
from database import db
from models import Login, Usuario
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="API MongoDB con FastAPI")

# --- Configurar CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especificar ["http://localhost:5173"] si usas Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rutas API ---
@app.get("/Home")
async def root():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/SignIn")
async def sign_in(datos: Login):
    usuario = await db["Usuario"].find_one({"email": datos.email})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario["contraseña"] != datos.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"mensaje": "Login exitoso", "nombre": usuario["nombre"]}


@app.get("/Usuarios", response_model=list[Usuario])
async def obtener_usuarios():
    usuarios = await db["Usuario"].find().to_list(100)
    return usuarios