import unittest

from controlador.controlador import ConfiguracionNivel, Controlador, FabricaNiveles
from motor.eventos import AdaptadorEventosMotor, ModeloObservable


# Doble del motor: registra llamadas sin ejecutar tablero, minas ni interfaz.
class MotorFalso:
    def __init__(self):
        self.aperturas = []
        self.banderas = []
        self.configuracion = None
        self.terminada = False

    def iniciar(self, filas, columnas, minas):
        self.configuracion = (filas, columnas, minas)

    def abrir(self, fila, columna):
        self.aperturas.append((fila, columna))
        return "abierto"

    def alternar_bandera(self, fila, columna):
        self.banderas.append((fila, columna))
        return "bandera"

    def partida_terminada(self):
        return self.terminada


# Doble de la vista: permite verificar notificaciones sin crear una ventana Tkinter.
class VistaFalsa:
    def __init__(self):
        self.eventos = []

    def actualizar(self, evento):
        self.eventos.append(evento)


class PruebasFactory(unittest.TestCase):
    def test_tres_niveles_clasicos(self):
        self.assertEqual((9, 9, 10), self._tupla("facil"))
        self.assertEqual((16, 16, 40), self._tupla("medio"))
        self.assertEqual((16, 30, 99), self._tupla("dificil"))

    def test_nivel_desconocido(self):
        with self.assertRaises(ValueError):
            FabricaNiveles.crear("experto")

    def test_configuracion_invalida(self):
        with self.assertRaises(ValueError):
            ConfiguracionNivel("Invalido", 1, 1, 1)

    def test_busca_nivel_sin_importar_mayusculas(self):
        configuracion = FabricaNiveles.crear("  FACIL  ")
        self.assertEqual("Fácil", configuracion.nombre)

    def test_registra_un_nivel_nuevo(self):
        personal = ConfiguracionNivel("Personalizado", 10, 12, 18)
        FabricaNiveles.registrar("personal", personal)

        self.assertIn("personal", FabricaNiveles.disponibles())
        self.assertIs(personal, FabricaNiveles.crear("PERSONAL"))

    @staticmethod
    def _tupla(nivel):
        configuracion = FabricaNiveles.crear(nivel)
        return configuracion.filas, configuracion.columnas, configuracion.minas


class PruebasControlador(unittest.TestCase):
    def setUp(self):
        self.motor = MotorFalso()
        self.controlador = Controlador(self.motor)

    def test_inicia_nivel_medio(self):
        configuracion = self.controlador.iniciar_partida("medio")

        self.assertEqual("Medio", configuracion.nombre)
        self.assertEqual((16, 16, 40), self.motor.configuracion)

    def test_abre_y_coloca_bandera(self):
        self.controlador.iniciar_partida("facil")

        self.assertEqual("abierto", self.controlador.abrir_casilla(1, 2))
        self.assertEqual("bandera", self.controlador.alternar_bandera(3, 4))
        self.assertEqual([(1, 2)], self.motor.aperturas)
        self.assertEqual([(3, 4)], self.motor.banderas)

    def test_bloquea_acciones_al_terminar(self):
        self.controlador.iniciar_partida("facil")
        self.motor.terminada = True

        self.assertIsNone(self.controlador.abrir_casilla(0, 0))
        self.assertIsNone(self.controlador.alternar_bandera(0, 0))
        self.assertEqual([], self.motor.aperturas)
        self.assertEqual([], self.motor.banderas)


class PruebasObserver(unittest.TestCase):
    def test_suscribe_notifica_y_desuscribe(self):
        modelo = ModeloObservable()
        vista = VistaFalsa()

        modelo.agregar_observador(vista)
        modelo.notificar("cambio", {"fila": 2})

        self.assertEqual(1, len(vista.eventos))
        self.assertEqual("cambio", vista.eventos[0].tipo)

        modelo.quitar_observador(vista)
        modelo.notificar("cambio")
        self.assertEqual(1, len(vista.eventos))

    def test_adaptador_con_callback_existente(self):
        clase_motor = type("MotorConCallback", (), {})
        motor = clase_motor()
        motor.recibidos = []
        motor.notificar = lambda tipo, **datos: motor.recibidos.append((tipo, datos))
        vista = VistaFalsa()

        adaptador = AdaptadorEventosMotor(motor, vista)
        adaptador.conectar()
        motor.notificar("Casillas descubiertas", casillas=[(1, 2)])

        self.assertEqual([("Casillas descubiertas", {"casillas": [(1, 2)]})], motor.recibidos)
        self.assertEqual("Casillas descubiertas", vista.eventos[0].tipo)
        self.assertEqual({"casillas": [(1, 2)]}, vista.eventos[0].datos)

        adaptador.desconectar()
        motor.notificar("bandera", fila=0, columna=1, puesta=True)
        self.assertEqual(1, len(vista.eventos))


if __name__ == "__main__":
    unittest.main()
