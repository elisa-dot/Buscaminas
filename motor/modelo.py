"""Archivo para el modelo del Buscaminas"""

from enum import Enum
from motor.minas import estrategiaMinas, minasAleatorias

DIRECCIONES = [ (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]


class Estado(Enum):
    EN_CURSO = "en curso"
    GANADO = "ganado"
    PERDIDO = "perdido"

class Casilla:
    def __init__(self):
        self.tiene_mina = False
        self.descubierta = False
        self.bandera = False
        self.minas_vecinas = 0

class Tablero:
    def __init__(self,filas,columnas,minas):
        if filas < 1 or columnas < 1:
            raise ValueError("Tablero no válido")

        self.filas = filas
        self.columnas = columnas
        self.casillas = []

        for _ in range(filas):
            for _ in range(columnas):
                fila.append(Casilla())
            self.casillas.append(fila)

        for f, c in minas:
            self.casillas[f][c].tiene_mina = True
        self.total_minas = len(minas)

        for f in range(filas):
            for c in range(columnas):
                contador = 0
                for vecino_f, vecino_c in self.vecinos(f,c):
                    if self.casillas[vecino_f][vecino_c].tiene_mina:
                        contador += 1
                self.casillas[f][c].minas_vecinas = contador

    def en_rango(self,f,c):
        return 0 <= f < self.filas and 0<= c <= self.columnas

    def casilla(self, f, c):
        if not self.en_rango(f,c):
            raise IndexError("Casilla no en el tablero")
        return self.casillas[f][c]

    def vecinos(self, f, c):
        resultado = []
        for posicion_f, posicion_c in DIRECCIONES:
            vecino_f,vecino_c = f + posicion_f, c + posicion_c
            if self.en_rango(vecino_f,vecino_c):
                resultado.append((vecino_f,vecino_c))
        return resultado

class Juego:
    def __init__(self,filas,columnas,minas,estrategia=NONE, mensaje=NONE):
        if estrategia is NONE:
            estrategia = minasAleatorias()
        
        if not isintance(estrategia, estrategiaMinas):
            raise TypeError("estrategia no válida")
        
        self.tablero = Tablero(filas,columnas, estrategia.colocar(filas,columnas,minas))
        self.estado = Estado.EN_CURSO
        self.jugadas = 0
        self.notificar = mensaje

    @property
    def terminado(self):
        return self.estado != Estado.EN_CURSO

    @property
    def banderas_puestas(self):
        return sum(c.bandera for fila in self.tablero.casillas for c in fila)
    @property
    def minas_restantes(self):
        return self.tablero.total_minas - self.banderas_puestas

    def emitir(self,evento, **datos):
        if self.notificar:
            self.notificar(evento, **datos)


    def descubrir(self,fila, columna):
        casilla = self.tablero.casilla(fila,columna)

        if self.terminado or casilla.bandera or casilla.descubierta:
            return []

        if self.jugadas == 0:
            self.emitir("Primera jugada")
        self.jugadas += 1

        if casilla.tiene_mina:
            casilla.descubierta = True
            self.estado = Estado.PERDIDO
            self.emitir("Perdiste")
            return [(fila,columna)]
        
        descubiertas = self.expandir(fila,columna)
        self.emitir("Casillas descubiertas", casillas = descubiertas)

        if self.casillas_sin_minas():
            self.estado = Estado.GANADO
            self.emitir("Ganaste")
        return descubiertas

    def expandir(self,fila,columna):
        descubiertas, sin_descubrir = [],[(fila,columna)]

        while sin_descubrir:
            sin_descubrir_f, sin_descubrir_c = sin_descubrir.pop()
            casilla = self.tablero.casillas[sin_descubrir_f][sin_descubrir_c]

            if casilla.descubierta or casilla.bandera or casilla.tiene_mina:
                continue
                
            casilla.descubierta = True
            descubiertas.append((sin_descubrir_f,sin_descubrir_c))

            if casilla.minas_vecinas == 0:
                sin_descubrir.extend(self.tablero.vecinos(sin_descubrir_f,sin_descubrir_c))

        return descubiertas

    def casillas_sin_minas(self):
        for fila in self.tablero.casillas:
            for casilla in fila:
                if not casilla.tiene_mina and not casilla.descubierta:
                    return False
        return True
    
    def alternar_bandera(self,fila,columna):
        casilla = self.tablero.casilla(fila,columna)
        if self.terminado or casilla.descubierta:
            return False
        
        casilla.bandera = not casilla.bandera
        self.emitir("bandera", fila = fila, columna = columna, puesta = casilla.bandera)

        return True

            
