'''
Vamos a dividir el código en un servidor de streaming y en un cliente.

El cliente únicamente tendrá un identificador e invocará los servicios del servidor.

El servidor de streaming:
   .- Tiene un catálogo de canciones, artistas y listas de reproducción.
   .- Por cada usuario mantiene un sistema de recomendación de elemntos de su catálogo.
   .- Los servicios que ofrece son:
     - reproducir_cancion(cancion_id)
     - asignar_recomendador(usuario_id)
     - generar_recomendacion(usuario_id), este servicio se delega al recomendador asignado al usuario.

El recomendador asignado a cada usuario se encarga de generar recomendaciones basadas en el 
historial de reproducciones del usuario. Para ello:
   .- Mantiene un registro de las canciones reproducidas por el usuario y una serie de 
     características y estadísticas de cada canción (género, artista, etc.).
   .- Cada vez que el usuario reproduce una canción, el recomendador actualiza su registro y las
     estadísticas asociadas a esa canción. Las difrentes estadísticas se van calculando
      por lotes aplicando un patrón cadena de responsabilidad sobre diferentes conjuntos de caracteristicas 
      de la canción.
   .- Utiliza un algoritmo de recomendación basado en la similitud entre las canciones reproducidas
      y las canciones del catálogo para generar recomendaciones personalizadas.
   .- La búsqueda del elemento a recomendar en el catálogo del servidor puede seguir tres estrategias:
     - Búsqueda aleatoria: selecciona un elemento del catálogo al azary si la similitud es suficiente, 
       la recomienda.
     - Búsqueda alfabética: recorre el catálogo en orden alfabético y recomienda el primer elemento
       que tenga una similitud suficiente.
     - Búsqueda cronológica: recorre el catálogo en orden cronológico y recomienda el primer elemento
       que tenga una similitud suficiente.
   .- El elemento del catálogo a recomendar es por defecto una canción, pero el recomendador también
      puede recomendar artistas o listas de reproducción. Estas recomendaciones se generan de forma 
      aditiva siguiendo un patrón decorador.

Patrones de diseño utilizados:
- R1: Singleton                 → SistemaRecomendacion (un único objeto por usuario)
- R2: Chain of Responsibility   → GeneradorEstadisticas (Audio → Sentimental, en cadena)
- R3: Decorator                 → Jerarquía GeneradorRecomendacion (enriquece la salida añadiendo
                                  canciones, artistas o playlists según lo configurado)
- R4: Strategy                  → Jerarquía EstrategiaBusqueda (Aleatoria / Temporal / Alfabética)
'''


from __future__ import annotations

import asyncio
import random
import statistics
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
from typing import Optional


# ─────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────

class CancionNoEncontradaError(Exception):
    """Se lanza cuando no existe una canción con el id indicado en el catálogo."""

class SinRecomendacionError(Exception):
    """Se lanza cuando no se encuentra ningún elemento que coincida con los estadísticos."""

class EstrategiaInvalidaError(Exception):
    """Se lanza cuando se proporciona una cadena de estrategia desconocida."""


# ─────────────────────────────────────────────
# ENUM GÉNERO MUSICAL
# ─────────────────────────────────────────────

class GeneroMusical(Enum):
    POP = "POP"
    ROCK = "ROCK"
    FOLK = "FOLK"
    CLASICA = "CLASICA"


# ─────────────────────────────────────────────
# MODELO DE DOMINIO
# ─────────────────────────────────────────────

class ElementoCatalogoMusical(ABC):
    """Clase base abstracta para todos los elementos del catálogo."""

    def __init__(self, id_: str, fecha: date):
        self.id: str = id_
        self.fecha: date = fecha
        # Estos diccionarios se calculan o asignan en las subclases
        self.caracteristicas_musicales: dict[str, float] = {}
        self.caracteristicas_sentimentales: dict[str, float] = {}

    # Método de conveniencia para obtener el nombre/título de forma uniforme
    @property
    @abstractmethod
    def display_elemento(self) -> str: ...


class Cancion(ElementoCatalogoMusical):
    def __init__(self,
                 id_: str,
                 titulo: str,
                 genero_musical: GeneroMusical,
                 duracion: int,
                 caracteristicas_musicales: dict[str, float],
                 caracteristicas_sentimentales: dict[str, float],
                 fecha_creacion: date):
        super().__init__(id_, fecha_creacion)
        self.titulo: str = titulo
        self.genero_musical: GeneroMusical = genero_musical
        self.duracion: int = duracion
        self.caracteristicas_musicales = caracteristicas_musicales
        self.caracteristicas_sentimentales = caracteristicas_sentimentales

    @property
    def display_elemento(self) -> str:
        return self.titulo

    def __repr__(self) -> str:
        return f"Cancion(id={self.id!r}, titulo={self.titulo!r})"


class Artista(ElementoCatalogoMusical):
    def __init__(self,
                 id_: str,
                 nombre: str,
                 genero_musical: GeneroMusical,
                 canciones: list[Cancion],
                 fecha_nacimiento: date):
        super().__init__(id_, fecha_nacimiento)
        self.nombre: str = nombre
        self.genero_musical: GeneroMusical = genero_musical
        self.canciones: list[Cancion] = canciones
        self._calcular_caracteristicas()

    def _calcular_caracteristicas(self) -> None:
        """Media de las características de todas sus canciones."""
        if not self.canciones:
            return
        # Lambda para calcular media de un atributo dado en una lista de dicts
        media_atributo = lambda dicts, clave: statistics.mean(
            d[clave] for d in dicts if clave in d
        )
        keys_mus = self.canciones[0].caracteristicas_musicales.keys()
        keys_sent = self.canciones[0].caracteristicas_sentimentales.keys()
        self.caracteristicas_musicales = {
            k: media_atributo([c.caracteristicas_musicales for c in self.canciones], k)
            for k in keys_mus
        }
        self.caracteristicas_sentimentales = {
            k: media_atributo([c.caracteristicas_sentimentales for c in self.canciones], k)
            for k in keys_sent
        }

    @property
    def display_elemento(self) -> str:
        return self.nombre

    def __repr__(self) -> str:
        return f"Artista(id={self.id!r}, nombre={self.nombre!r})"


class Playlist(ElementoCatalogoMusical):
    def __init__(self,
                 id_: str,
                 titulo: str,
                 canciones: list[Cancion],
                 fecha_creacion: date):
        super().__init__(id_, fecha_creacion)
        self.titulo: str = titulo
        self.canciones: list[Cancion] = canciones
        self._calcular_caracteristicas()

    def _calcular_caracteristicas(self) -> None:
        """Media de las características de todas sus canciones."""
        if not self.canciones:
            return
        media_atributo = lambda dicts, clave: statistics.mean(
            d[clave] for d in dicts if clave in d
        )
        keys_mus = self.canciones[0].caracteristicas_musicales.keys()
        keys_sent = self.canciones[0].caracteristicas_sentimentales.keys()
        self.caracteristicas_musicales = {
            k: media_atributo([c.caracteristicas_musicales for c in self.canciones], k)
            for k in keys_mus
        }
        self.caracteristicas_sentimentales = {
            k: media_atributo([c.caracteristicas_sentimentales for c in self.canciones], k)
            for k in keys_sent
        }

    @property
    def display_elemento(self) -> str:
        return self.titulo

    def __repr__(self) -> str:
        return f"Playlist(id={self.id!r}, titulo={self.titulo!r})"
    


# ─────────────────────────────────────────────
# CATÁLOGO MUSICAL
# ─────────────────────────────────────────────

class CatalogoMusical:
    """Repositorio central con canciones, artistas y playlists."""

    def __init__(self):
        self.canciones: list[Cancion] = []
        self.playlists: list[Playlist] = []
        self.artistas: list[Artista] = []

    def __repr__(self) -> str:
        return (f"CatalogoMusical("
                f"{len(self.canciones)} canciones, "
                f"{len(self.artistas)} artistas, "
                f"{len(self.playlists)} playlists)")    


# ─────────────────────────────────────────────
# PATRÓN CHAIN OF RESPONSIBILITY – R2
# GeneradorEstadisticas
# ─────────────────────────────────────────────

class GeneradorEstadisticas(ABC):
    """
    Nodo abstracto de la cadena.
    Cada nodo procesa su familia de características y pasa el control al siguiente.
    """

    def __init__(self):
        self._estadistico: Optional[GeneradorEstadisticas] = None

    def set_next(self, siguiente: GeneradorEstadisticas) -> GeneradorEstadisticas:
        self._estadistico = siguiente
        return siguiente

    @abstractmethod
    def generar_estadistica(self, cancion: Cancion) -> dict[str, float]:
        """Calcula estadísticos para esta canción y opcionalmente delega al siguiente."""
        ...

    # Función de orden superior: calcula media y desviación de una lista de valores
    # Una función de orden superior debería: (1) aceptar una función como argumento o (2) devolver una función.
    @staticmethod
    def _estadisticos_lista(valores: list[float]) -> dict[str, float]:
        if not valores:
            return {"media": 0.0, "desviacion": 0.0}
        media = statistics.mean(valores)
        desv = statistics.stdev(valores) if len(valores) > 1 else 0.0
        return {"media": media, "desviacion": desv}


class GeneradorEstadisticasAudio(GeneradorEstadisticas):
    """Calcula estadísticos sobre características SONORAS."""

    def __init__(self):
        super().__init__()
        self._historial: list[dict[str, float]] = []

    def generar_estadistica(self, cancion: Cancion) -> dict[str, float]:
        self._historial.append(cancion.caracteristicas_musicales)
        # Función de orden superior: aplica _estadisticos_lista por cada clave
        resultado = {}
        if self._historial:
            claves = self._historial[0].keys()
            for clave in claves:
                valores = list(map(lambda d: d.get(clave, 0.0), self._historial))
                stats = self._estadisticos_lista(valores)
                resultado[f"audio_{clave}_media"] = stats["media"]
                resultado[f"audio_{clave}_desv"] = stats["desviacion"]

        # Delegar al siguiente eslabón de la cadena
        if self._estadistico:
            resultado.update(self._estadistico.generar_estadistica(cancion))
        return resultado


class GeneradorEstadisticasSentimentales(GeneradorEstadisticas):
    """Calcula estadísticos sobre características SENTIMENTALES."""

    def __init__(self):
        super().__init__()
        self._historial: list[dict[str, float]] = []

    def generar_estadistica(self, cancion: Cancion) -> dict[str, float]:
        self._historial.append(cancion.caracteristicas_sentimentales)
        resultado = {}
        if self._historial:
            claves = self._historial[0].keys()
            for clave in claves:
                valores = list(map(lambda d: d.get(clave, 0.0), self._historial))
                stats = self._estadisticos_lista(valores)
                resultado[f"sent_{clave}_media"] = stats["media"]
                resultado[f"sent_{clave}_desv"] = stats["desviacion"]

        if self._estadistico:
            resultado.update(self._estadistico.generar_estadistica(cancion))
        return resultado



# ─────────────────────────────────────────────
# PATRÓN STRATEGY – R4
# EstrategiaBusqueda
# ─────────────────────────────────────────────

def _match(elemento: ElementoCatalogoMusical,
           caracteristicas_sesion: dict[str, float],
           umbral: float = 0.50) -> bool:
    """
    Función auxiliar que comprueba si un elemento del catálogo
    'hace match' con los estadísticos de la sesión actual.
    Estrategia simple: distancia euclídea normalizada < umbral.
    """
    # Extraemos medias de audio y sentimentales de la sesión
    def media_sesion(prefijo: str, diccionario: dict[str, float]) -> dict[str, float]:
        return {k.replace(prefijo, ""): v
                for k, v in diccionario.items() if k.endswith("_media") and k.startswith(prefijo)}

    medias_audio = media_sesion("audio_", caracteristicas_sesion)
    medias_sent = media_sesion("sent_", caracteristicas_sesion)

    # Distancia sobre características musicales
    distancia = 0.0
    n = 0
    for clave, val_sesion in medias_audio.items():
        val_elem = elemento.caracteristicas_musicales.get(clave, 0.0)
        distancia += (val_sesion - val_elem) ** 2
        n += 1
    for clave, val_sesion in medias_sent.items():
        val_elem = elemento.caracteristicas_sentimentales.get(clave, 0.0)
        distancia += (val_sesion - val_elem) ** 2
        n += 1

    if n == 0:
        return True
    distancia = (distancia / n) ** 0.5
    return distancia < umbral





class Cliente:

    def __init__(self, usuario_id):
        self.usuario_id = usuario_id

    # stub para invocar los servicios del servidor
    def reproducir_cancion(self, cancion_id):
        # Lógica para reproducir la canción
        pass

    # stub para invocar los servicios del servidor
    def asignar_recomendador(self, recomendador):
        self.recomendador = recomendador

    # stub para invocar los servicios del servidor
    def generar_recomendacion(self):
        return self.recomendador.generar_recomendacion(self.usuario_id)