"""Controller y coordinación MVC del Buscaminas."""

from __future__ import annotations

from typing import Protocol

from .niveles import ConfiguracionNivel, FabricaNiveles


class MotorBuscaminas(Protocol):
    def abrir(self, fila: int, columna: int) -> object: ...

    def alternar_bandera(self, fila: int, columna: int) -> object: ...

    def partida_terminada(self) -> bool: ...


class Controlador:
    """Coordina acciones de la vista con el motor sin contener reglas del juego."""

    def __init__(
        self,
        motor,
        fabrica: type[FabricaNiveles] = FabricaNiveles,
    ) -> None:
        self.motor = motor
        self.fabrica = fabrica
        self.nivel_actual: ConfiguracionNivel | None = None

    def iniciar_partida(self, nivel: str) -> ConfiguracionNivel:
        configuracion = self.fabrica.crear(nivel)
        self.nivel_actual = configuracion

        # Admite dos nombres de API para facilitar la integración con el motor.
        metodo = getattr(self.motor, "iniciar", None)
        if metodo is not None:
            metodo(configuracion.filas, configuracion.columnas, configuracion.minas)
        else:
            metodo_nuevo = getattr(self.motor, "nueva_partida", None)
            if metodo_nuevo is not None:
                metodo_nuevo(configuracion.filas, configuracion.columnas, configuracion.minas)

        return configuracion

    def abrir_casilla(self, fila: int, columna: int) -> object:
        # El Controller impide acciones posteriores a victoria o derrota.
        if self._partida_terminada():
            return None

        metodo = getattr(self.motor, "abrir", None)
        if metodo is not None:
            return metodo(fila, columna)

        metodo_casilla = getattr(self.motor, "descubrir_casilla", None)
        if metodo_casilla is not None:
            return metodo_casilla(fila, columna)

        raise AttributeError("El motor no ofrece una operación para abrir casillas")

    def alternar_bandera(self, fila: int, columna: int) -> object:
        if self._partida_terminada():
            return None

        metodo = getattr(self.motor, "alternar_bandera", None)
        if metodo is not None:
            return metodo(fila, columna)

        metodo_bandera = getattr(self.motor, "poner_quitar_bandera", None)
        if metodo_bandera is not None:
            return metodo_bandera(fila, columna)

        raise AttributeError("El motor no ofrece una operación para alternar banderas")

    def _partida_terminada(self) -> bool:
        # Delegamos el estado final al motor; el Controller no repite sus reglas.
        metodo = getattr(self.motor, "partida_terminada", None)
        if metodo is None:
            return False
        return bool(metodo())
