"""Contratos y eventos para actualizar observadores del modelo.

El motor publica eventos sin conocer Tkinter ni ninguna clase de interfaz.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class Observador(Protocol):
    """Interfaz mínima que debe implementar una vista que observe el modelo."""

    def actualizar(self, evento: "EventoModelo") -> None:
        ...


@dataclass(frozen=True)
class EventoModelo:
    """Descripción inmutable de un cambio publicado por el motor."""

    tipo: str
    datos: object | None = None


class ModeloObservable:
    """Base opcional para añadir suscripciones a una clase del motor.

    Las clases de modelo pueden heredar de ella o reproducir la interfaz
    agregar_observador/quitar_observador/notificar.
    """

    def __init__(self) -> None:
        self._observadores: list[Observador] = []

    def agregar_observador(self, observador: Observador) -> None:
        # Evita suscripciones duplicadas para una misma vista.
        if not isinstance(observador, Observador):
            raise TypeError("El observador debe implementar actualizar(evento)")
        if observador not in self._observadores:
            self._observadores.append(observador)

    def quitar_observador(self, observador: Observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, tipo: str, datos: object | None = None) -> None:
        evento = EventoModelo(tipo=tipo, datos=datos)
        # La copia permite desuscribirse durante la actualización sin romper el ciclo.
        for observador in tuple(self._observadores):
            observador.actualizar(evento)
