""" Archivo minas, para definir las posiciones de las minas, ocupamos el patron strategy
"""
import random
from abc import ABC, abstractmethod

class estrategiaMinas(ABC):
    @abstractmothod
    def colocar(self, filas, columnas, cantidad):
        ...

class minasAleatorias(estrategiaMinas):
    def __init__(self, valor_inicial=None):
        self._rdm = random.Random(valor_inicial)

    def colocar(self, filas, columnas, cantidad):
        if cantidad >= filas * columnas:
            raise ValueError("La cantidad de minas excede el tamaño del tablero")
        
        posiciones_tablero = []

        for f in range(filas):
            for c in range(columnas):
                possiciones_tablero.append((f,c))

        return set(self._rdm.sample(posiciones_tablero,cantidad))

"""Método para colocar las minas de una manera fija"""
class minasFijas(estrategiaMinas):
    def __init__(self, posiciones):
        self._posiciones = set(posiciones)

    def colocar(self, filas, columnas, cantidad = None):
        for f,c in self._posiciones:
            if nor (0 <= f < filas and 0 <= c< columnas):
                raise ValueError(f"Mina fiera del tablero")
            return set(self._posiciones)
    


