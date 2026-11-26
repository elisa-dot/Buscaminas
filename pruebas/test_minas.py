import unittest

from motor.minas import minasAleatorias, minasFijas
from motor.modelo import Estado, Juego, Tablero

def juego(filas, columnas, minas, notificar =None):
    return Juego(filas, columnas, len(minas), minasFijas(minas), notificar)

class PruebasMinas(unittest.TestCase):
    """Prueba para detectar que s pongan la cantidad correcta de minas"""
    def test_minas_fijas(self):
        a = minasAleatorias(1).colocar(9,9,10)
        b = minasAleatorias(1).colocar(9,9,10)
        self.assertEqual(len(a),10)
        self.assertEqual(a,b)
    
    """Prueba para detectar si la cantidad de las minas aleatorias son las pedidas"""
    def test_minas_aleatorias(self):
        a = Juego(9,9,10,minasAleatorias(3))
        b = Juego(9,9,10,minasAleatorias(3))

        self.assertEqual(len(self.minas_en_tablero(a)),10)
        self.assertEqual(a.tablero.total_minas,10)
        self.assertEqual(self.minas_en_tablero(a), self.minas_en_tablero(b))

    """Prueba para detectar qu eninguna mina se ponga fuera del tablero"""
    def test_fuera_tablero(self):
        with self.assertRaises(ValueError):
            minasFijas({(9,9)}).colocar(3,3)
    
    def minas_en_tablero(self,j):
        resultado = set()

        for f in range(j.tablero.filas):
            for c in range(j.tablero.columnas):
                if j.tablero.casillas[f][c].tiene_mina:
                    resultado.add((f,c))
        
        return resultado
    
    """Prueba para detectar sin las minas quedan en las posicione sdadas"""
    def test_minas_lugar_correcto(self):
        j = juego(3,3,{(0,0),(2,2)})
        self.assertEqual(self.minas_en_tablero(j), {(0,0),(2,2)})
        self.assertFalse(j.tablero.casilla(1,1).tiene_mina)
        self.assertEqual(j.tablero.total_minas, 2)

if __name__ == "__main__":
    unittest.main()