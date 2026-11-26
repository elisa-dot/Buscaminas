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
    
class PruebasMinasVecinas(unittest.TestCase):

    """Prueba para verificar la cantidad de vecinos, esquinas, orillas, centro"""
    def test_cantidad_de_vecinos(self):
        tablero = Tablero(3,3,set())
        self.assertEqual(len(tablero.vecinos(0,0)) ,3)
        self.assertEqual(len(tablero.vecinos(0,1)),5)
        self.assertEqual(len(tablero.vecinos(1,1)), 8)

    """Prueba para verificar la cantidad de minas vecinas"""
    def test_cantidad_de_minas_vecinas(self):
        tablero = Tablero(3,3,{(0,0),(2,2)})
        self.assertEqual(tablero.casilla(1,1).minas_vecinas,2)
        self.assertEqual(tablero.casilla(0,1).minas_vecinas,1)
        self.assertEqual(tablero.casilla(0,2).minas_vecinas,0)
    
    """Prueba para verificar que la expansion se detiene en minas"""
    def test_expansion_detiene_en_mina(self):
        j = juego(4,4,{(3,3)})
        descubiertas = j.descubrir(0,0)
        self.assertEqual(len(descubiertas), 15)
    
    """Prueba para verificar la expansion se detiene en numeros"""
    def test_expansion_detiene_en_numeros(self):
        j = juego(1,5, {(0,4)})
        j.descubrir(0,0)
        self.assertTrue(j.tablero.casilla(0,3).descubierta)
        self.assertFalse(j.tablero.casilla(0,4).descubierta)
    
    """Prueba para verificar que al descubrir casilla con número, solo se descubre esta"""
    def test_numero_no_expande(self):
        j = juego(3,3,{(0,0)})
        self.assertEqual(j.descubrir(1,1), [(1,1)])

    """Prueba para verificar que cuando hay bandera la expansion se detiene"""
    def test_expansion_no_abre_banderas(self):
        j = juego(3,3,{(2,2)})
        j.alternar_bandera(0,1)
        j.descubrir(0,0)
        self.assertFalse(j.tablero.casilla(0,1).descubierta)

class PruebasBanderas(unittest.TestCase):

    """Prueba oara comprobar que la bandera se quita y se pone"""
    def test_poner_y_quitar_banderas(self):
        j = juego(3,3,{(0,0)})
        self.assertTrue(j.alternar_bandera(1,1))
        self.assertEqual(j.minas_restantes,0)
        j.alternar_bandera(1,1)
        self.assertEqual(j.minas_restantes,1)

    """Prueba para comprobar que la casilla con bandera no se descubre"""
    def test_casilla_con_bandera_no_se_descubre(self):
        j = juego(3,3,{(0,0)})
        j.alternar_bandera(0,0)
        self.assertEqual(j.descubrir(0,0),[])
        self.assertEqual(j.estado, Estado.EN_CURSO)
    
    """Prueba para comprobar que no se puedan poner banderas en casillas ya descubiertas"""
    def test_no_bandera_en_casilla_descubierta(self):
        j = juego(3,3,{(0,0)})
        j.descubrir(1,1)
        self.assertFalse(j.alternar_bandera(1,1))
    
class PruebasFinDelJuego(unittest.TestCase):

    """Prueba para comprobar que ya ha perdido"""
    def test_derrota(self):
        j = juego(3,3,{(0,0)})
        j.descubrir(0,0)
        self.assertEqual(j.estado, Estado.PERDIDO)

    """Prueba para comprobar que ha ganado"""

    def test_victoria(self):
        j = juego(2,2,{(0,0)})
        j.descubrir(0,1)
        j.descubrir(1,0)
        self.assertEqual(j.estado, Estado.EN_CURSO)
        j.descubrir(1,1)
        self.assertEqual(j.estado, Estado.GANADO)

    """Prueba para comprobar que cunado pierdas ya no puedas hacer nada"""
    def test_bloqueo_tras_derrota(self):
        j = juego(3,3,{(0,0)})
        j.descubrir(0,0)
        self.assertEqual(j.descubrir(2,2),[])
        self.assertFalse(j.alternar_bandera(2,2))

    """Prueba para comprobar uqe cuando ganes ya no puedas hacer nada"""
    def test_bloqueo_tras_victoria(self):
        j = juego(1,2,{(0,0)})
        j.descubrir(0,1)
        self.assertTrue(j.terminado)
        self.assertFalse(j.alternar_bandera(0,0))
    
    """Prueba para mandar error cuando la casilla que se quiere descubrir esta fuera del tablero"""
    def test_fuera_tablero(self):
        j = juego(3,3,{(0,0)})
        with self.assertRaises(IndexError):
            j.descubrir(5,5)
    

if __name__ == "__main__":
    unittest.main()