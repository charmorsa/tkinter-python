# models.py
from pydantic import BaseModel

class Usuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    contraseña: str
    dni: float
    estado: bool


##  Interface
class Login(BaseModel):
    email: str
    password: str