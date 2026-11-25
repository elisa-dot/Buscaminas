"""Archivo para el modelo del Buscaminas"""

form enum import enum
from motor.minas import estrategiaMinas, minasAleatorias

class Estado(Enum):
    EN_CURSO = "en curso"
    GANADO = "ganado"
    PERDIDO = "perdido"