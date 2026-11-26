# Proyecto 2: Buscaminas

Modelado y Programación — Grupo 7078, Semestre 2027-1

## Descripción

Este proyecto implementa el juego Buscaminas con interfaz gráfica. El motor del juego está separado de la interfaz siguiendo el patrón Modelo-Vista-Controlador (MVC), y se aplican los patrones de diseño Observer, Strategy y Factory.

| Nivel | Filas × columnas | Minas |
|-------|------------------|-------|
| Fácil | 9 × 9 | 10 |
| Medio | 16 × 16 | 40 |
| Difícil | 16 × 30 | 99 |

## Equipo

- Elisa Cuevas Ferreira — 322087129
- Cynthia Uribe Martínez — 322128427
- Gael Bensussen González — 322018424

## Requisitos

- Python 3.10 o superior
- Tkinter (viene incluido con Python)

En Fedora, si Tkinter no está instalado:

```bash
sudo dnf install python3-tkinter
```

El proyecto no necesita instalar dependencias externas. Las pruebas usan `unittest`, que ya viene con Python.

## Estructura del proyecto

```
Buscaminas/
├── README.md
├── motor/
│   ├── __init__.py
│   ├── main.py
│   ├── modelo.py
│   ├── minas.py
│   ├── eventos.py
│   └── niveles.py
├── controlador/
│   ├── __init__.py
│   └── controlador.py
├── interfaz/
│   ├── __init__.py
│   ├── aplicacion.py
│   └── tablero.py
├── tests/
│   ├── __init__.py
│   └──
└── docs/
    ├── reporte_tecnico.pdf
    └── reporte_modelado_de_lenguaje.pdf
```


## Cómo ejecutar

Desde la carpeta raíz del proyecto:

```bash
python3 main.py
```

## Cómo jugar

- **Clic izquierdo:** descubrir una casilla.
- **Clic derecho:** colocar o quitar una bandera.
- Al descubrir una casilla vacía se descubren automáticamente sus vecinos.
- Se gana al descubrir todas las casillas sin mina. Se pierde al descubrir una mina, y entonces se muestran todas.
- El temporizador empieza con la primera jugada y se detiene al terminar la partida.
- Para empezar de nuevo se puede usar el botón de nueva partida y elegir el nivel.



## Arquitectura

- **Modelo (`motor/`):** reglas del juego, independiente de la interfaz. No importa Tkinter.
- **Vista (`interfaz/`):** ventana, tablero, temporizador y captura de clics.
- **Controlador (`controlador/`):** conecta los clics de la vista con el modelo y maneja el temporizador.

Patrones de diseño usados:

| Patrón | Para qué se usa | Dónde está |
|--------|-----------------|------------|
| Observer | La vista se actualiza cuando cambia el modelo | `motor/eventos.py` |
| Strategy | Colocación de minas (aleatoria o fija para pruebas) | `motor/minas.py` |
| Factory | Crear el juego según el nivel de dificultad | `motor/niveles.py` |

Los detalles completos del diseño y los supuestos están en `docs/reporte_tecnico.pdf`, y el uso de modelos de lenguaje durante el desarrollo está documentado en `docs/REPORTE_LM.md`.

## Pruebas

Las pruebas unitarias del motor se ejecutan desde la raíz del proyecto con:

```bash
python3 -m unittest discover pruebas -v
```

| Archivo | Qué verifica |
|---------|--------------|
| `test_modelo.py` | Vecinos, expansión automática (orillas y esquinas), banderas, victoria, derrota y bloqueo al terminar |
| `test_minas.py` | Colocación de minas aleatoria y fija |
| `test_eventos.py` | Que los observadores reciban los eventos |
| `test_niveles.py` | Que la fábrica cree los tres niveles con el tamaño y las minas correctos |

## Pruebas manuales de la interfaz

- Los tres niveles se pueden elegir y el tablero tiene el tamaño correcto.
- El clic izquierdo descubre y el derecho pone o quita bandera.
- Una casilla vacía expande a sus vecinos sin pasar por banderas.
- Al perder se muestran todas las minas y el tablero deja de responder.
- Al ganar el tablero deja de responder.
- El temporizador inicia con la primera jugada y se detiene al terminar.
- El botón de nueva partida reinicia el tablero y el temporizador.

