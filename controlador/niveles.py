"""Configuración y creación de niveles del Buscaminas."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionNivel:
    """Datos mínimos necesarios para construir un tablero."""

    nombre: str
    filas: int
    columnas: int
    minas: int

    def __post_init__(self) -> None:
        # Evita crear niveles con dimensiones o cantidades de minas imposibles.
        if self.filas <= 0 or self.columnas <= 0:
            raise ValueError("El tablero debe tener filas y columnas positivas")
        if self.minas < 0:
            raise ValueError("La cantidad de minas no puede ser negativa")
        if self.minas >= self.filas * self.columnas:
            raise ValueError("Debe existir al menos una casilla sin mina")


class FabricaNiveles:
    """Factory extensible para los niveles disponibles."""

    # Registrar niveles permite ampliarlos sin modificar el Controller.
    _NIVELES: dict[str, ConfiguracionNivel] = {
        "facil": ConfiguracionNivel("Fácil", 9, 9, 10),
        "medio": ConfiguracionNivel("Medio", 16, 16, 40),
        "dificil": ConfiguracionNivel("Difícil", 16, 30, 99),
    }

    @classmethod
    def crear(cls, nivel: str) -> ConfiguracionNivel:
        clave = cls._normalizar(nivel)
        try:
            return cls._NIVELES[clave]
        except KeyError as error:
            raise cls.nivel_desconocido(nivel) from error

    @classmethod
    def registrar(cls, clave: str, configuracion: ConfiguracionNivel) -> None:
        """Agrega o reemplaza un nivel usando su clave normalizada."""

        clave_normalizada = cls._normalizar(clave)
        if not clave_normalizada:
            raise ValueError("La clave del nivel no puede estar vacía")
        cls._NIVELES[clave_normalizada] = configuracion

    @classmethod
    def disponibles(cls) -> tuple[str, ...]:
        return tuple(cls._NIVELES)

    @classmethod
    def nivel_desconocido(cls, nivel: str) -> ValueError:
        disponibles = ", ".join(cls.disponibles())
        return ValueError(
            f"Nivel desconocido: {nivel}. Opciones: {disponibles}"
        )

    @staticmethod
    def _normalizar(nivel: str) -> str:
        if not isinstance(nivel, str):
            raise ValueError("El nivel debe indicarse como texto")
        return nivel.strip().lower()
