"""
Sistema de Recomendación Musical
=================================
Patrones de diseño utilizados:
- R1: Singleton       → SistemaRecomendacion (un único objeto por usuario)
- R2: Chain of Responsibility → GeneradorEstadisticas (Audio → Sentimental, en cadena)
- R3: Decorator       → Jerarquía GeneradorRecomendacion (enriquece la salida añadiendo
                         canciones, artistas o playlists según lo configurado)
- R4: Strategy        → Jerarquía EstrategiaBusqueda (Aleatoria / Temporal / Alfabética)
"""

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

    def __init__(self, id_: str, fecha_creacion_nacimiento: date):
        self.id: str = id_
        self.fecha_creacion_nacimiento: date = fecha_creacion_nacimiento
        # Estos diccionarios se calculan o asignan en las subclases
        self.caracteristicas_musicales: dict[str, float] = {}
        self.caracteristicas_sentimentales: dict[str, float] = {}

    # Método de conveniencia para obtener el nombre/título de forma uniforme
    @property
    @abstractmethod
    def nombre_display(self) -> str: ...


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
    def nombre_display(self) -> str:
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
    def nombre_display(self) -> str:
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
    def nombre_display(self) -> str:
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


class EstrategiaBusqueda(ABC):
    """Interfaz Strategy."""

    def __init__(self, catalogo: CatalogoMusical):
        self._catalogo = catalogo

    @abstractmethod
    def buscar_elemento_catalogo(self,
                                 caracteristicas_sesion: dict,
                                 tipo: str) -> Optional[ElementoCatalogoMusical]:
        """
        Busca un elemento (cancion / artista / playlist) en el catálogo
        que coincida con los estadísticos de la sesión.
        """
        ...

    def _lista_por_tipo(self, tipo: str) -> list[ElementoCatalogoMusical]:
        if tipo == "cancion":
            return list(self._catalogo.canciones)
        elif tipo == "artista":
            return list(self._catalogo.artistas)
        elif tipo == "playlist":
            return list(self._catalogo.playlists)
        raise ValueError(f"Tipo desconocido: {tipo!r}")


class BusquedaAleatoria(EstrategiaBusqueda):
    """Selecciona elementos al azar hasta encontrar uno que haga match."""

    def buscar_elemento_catalogo(self,
                                 caracteristicas_sesion: dict,
                                 tipo: str) -> Optional[ElementoCatalogoMusical]:
        elementos = self._lista_por_tipo(tipo)
        if not elementos:
            return None
        intentados: set = set()
        while len(intentados) < len(elementos):
            candidato = random.choice(elementos)
            if candidato.id in intentados:
                continue
            intentados.add(candidato.id)
            if _match(candidato, caracteristicas_sesion):
                return candidato
        return None


class BusquedaOrdenTemporal(EstrategiaBusqueda):
    """Ordena de más nuevo a más antiguo y devuelve el primer match."""

    def buscar_elemento_catalogo(self,
                                 caracteristicas_sesion: dict,
                                 tipo: str) -> Optional[ElementoCatalogoMusical]:
        elementos = sorted(
            self._lista_por_tipo(tipo),
            key=lambda e: e.fecha_creacion_nacimiento,
            reverse=True          # más nuevo primero
        )
        # Función de orden superior: filter + next
        return next(filter(lambda e: _match(e, caracteristicas_sesion), elementos), None)


class BusquedaOrdenAlfabetico(EstrategiaBusqueda):
    """Ordena alfabéticamente (A→Z) y devuelve el primer match."""

    def buscar_elemento_catalogo(self,
                                 caracteristicas_sesion: dict,
                                 tipo: str) -> Optional[ElementoCatalogoMusical]:
        elementos = sorted(
            self._lista_por_tipo(tipo),
            key=lambda e: e.nombre_display.lower()
        )
        return next(filter(lambda e: _match(e, caracteristicas_sesion), elementos), None)


# ─────────────────────────────────────────────
# PATRÓN DECORATOR – R3
# GeneradorRecomendacion
# ─────────────────────────────────────────────

class GeneradorRecomendacion(ABC):
    """Componente base del patrón Decorator."""

    def __init__(self):
        self._estrategia_busqueda: Optional[EstrategiaBusqueda] = None

    def establecer_estrategia(self, estrategia: EstrategiaBusqueda) -> None:
        self._estrategia_busqueda = estrategia

    @abstractmethod
    def recomendar(self, caracteristicas_sesion: dict) -> dict[str, ElementoCatalogoMusical]:
        """Devuelve un dict con claves 'cancion', 'artista', 'playlist' según la configuración."""
        ...


class GeneradorRecomendacionCanciones(GeneradorRecomendacion):
    """Componente concreto base: siempre recomienda una canción."""

    def recomendar(self, caracteristicas_sesion: dict) -> dict[str, ElementoCatalogoMusical]:
        if self._estrategia_busqueda is None:
            raise SinRecomendacionError("No se ha establecido una estrategia de búsqueda.")
        cancion = self._estrategia_busqueda.buscar_elemento_catalogo(caracteristicas_sesion, "cancion")
        if cancion is None:
            raise SinRecomendacionError("No se encontró ninguna canción que coincida con la sesión.")
        return {"cancion": cancion}


class GeneradorRecomendacionMejorado(GeneradorRecomendacion):
    """Decorador abstracto base."""

    def __init__(self, wrapped: GeneradorRecomendacion):
        super().__init__()
        self._wrapped = wrapped

    def establecer_estrategia(self, estrategia: EstrategiaBusqueda) -> None:
        """Propaga la estrategia al componente envuelto y a sí mismo."""
        super().establecer_estrategia(estrategia)
        self._wrapped.establecer_estrategia(estrategia)

    def recomendar(self, caracteristicas_sesion: dict) -> dict[str, ElementoCatalogoMusical]:
        return self._wrapped.recomendar(caracteristicas_sesion)


class GeneradorRecomendacionPlaylist(GeneradorRecomendacionMejorado):
    """Decorador concreto: enriquece la recomendación añadiendo una playlist."""

    def recomendar(self, caracteristicas_sesion: dict) -> dict[str, ElementoCatalogoMusical]:
        resultado = super().recomendar(caracteristicas_sesion)
        playlist = self._estrategia_busqueda.buscar_elemento_catalogo(caracteristicas_sesion, "playlist")
        if playlist is None:
            raise SinRecomendacionError("No se encontró ninguna playlist que coincida.")
        resultado["playlist"] = playlist
        return resultado


class GeneradorRecomendacionArtista(GeneradorRecomendacionMejorado):
    """Decorador concreto: enriquece la recomendación añadiendo un artista."""

    def recomendar(self, caracteristicas_sesion: dict) -> dict[str, ElementoCatalogoMusical]:
        resultado = super().recomendar(caracteristicas_sesion)
        artista = self._estrategia_busqueda.buscar_elemento_catalogo(caracteristicas_sesion, "artista")
        if artista is None:
            raise SinRecomendacionError("No se encontró ningún artista que coincida.")
        resultado["artista"] = artista
        return resultado


# ─────────────────────────────────────────────
# PATRÓN SINGLETON – R1
# SistemaRecomendacion
# ─────────────────────────────────────────────

class SistemaRecomendacion:
    """
    Singleton: garantiza una única instancia de recomendador por usuario.
    La instancia se almacena en _recomendadores (dict usuario_id → instancia).
    """

    _recomendadores: dict[str, SistemaRecomendacion] = {}

    def __new__(cls, usuario_id: str):
        if usuario_id not in cls._recomendadores:
            instancia = super().__new__(cls)
            instancia._inicializado = False
            cls._recomendadores[usuario_id] = instancia
        return cls._recomendadores[usuario_id]

    def __init__(self, usuario_id: str):
        if self._inicializado:
            return
        self._inicializado = True
        self.usuario_id: str = usuario_id
        self.caracteristicas_sesion_actual: dict[str, float] = {}
        self.target_element: str = "cancion"    # por defecto
        self.estrategia: str = "aleatoria"       # por defecto
        self.canciones_escuchadas: list[Cancion] = []

        # Cadena de responsabilidad para los estadísticos
        self._generador_audio = GeneradorEstadisticasAudio()
        self._generador_sent = GeneradorEstadisticasSentimentales()
        self._generador_audio.set_next(self._generador_sent)

        # Generador de recomendaciones (se construye en configurar_recomendador)
        self._generador_recomendacion: Optional[GeneradorRecomendacion] = None
        self._catalogo: Optional[CatalogoMusical] = None

    # ── Configuración ────────────────────────────────────────────────────────

    def configurar_recomendador(self,
                                catalogo: CatalogoMusical,
                                target_element: str,
                                estrategia: str) -> None:
        """
        Configura qué se recomienda (cancion / cancion+artista / cancion+playlist /
        cancion+artista+playlist) y la estrategia de búsqueda.
        """
        self._catalogo = catalogo
        self.target_element = target_element
        self.estrategia = estrategia

        # Construir la estrategia de búsqueda (Strategy)
        estrategias_map = {
            "aleatoria": BusquedaAleatoria,
            "temporal": BusquedaOrdenTemporal,
            "alfabetica": BusquedaOrdenAlfabetico,
        }
        if estrategia not in estrategias_map:
            raise EstrategiaInvalidaError(
                f"Estrategia {estrategia!r} no reconocida. "
                f"Opciones válidas: {list(estrategias_map.keys())}"
            )
        estrategia_obj = estrategias_map[estrategia](catalogo)

        # Construir el generador de recomendaciones con decoradores (Decorator)
        generador: GeneradorRecomendacion = GeneradorRecomendacionCanciones()
        if "playlist" in target_element:
            generador = GeneradorRecomendacionPlaylist(generador)
        if "artista" in target_element:
            generador = GeneradorRecomendacionArtista(generador)

        generador.establecer_estrategia(estrategia_obj)
        self._generador_recomendacion = generador

    # ── Escucha de canciones (asíncrono) ─────────────────────────────────────

    async def escuchar_cancion(self, cancion_id: str) -> None:
        """
        Recibe una canción (por id) y actualiza los estadísticos de la sesión
        mediante la cadena de responsabilidad de forma asíncrona.
        """
        if self._catalogo is None:
            raise RuntimeError("El catálogo no ha sido configurado.")

        # Buscar la canción en el catálogo (función lambda de búsqueda)
        buscar = lambda canciones, cid: next((c for c in canciones if c.id == cid), None)
        cancion = buscar(self._catalogo.canciones, cancion_id)
        if cancion is None:
            raise CancionNoEncontradaError(
                f"No existe ninguna canción con id {cancion_id!r} en el catálogo."
            )

        self.canciones_escuchadas.append(cancion)

        # Simular operación asíncrona (p.ej., consulta a un servicio externo)
        await asyncio.sleep(0)

        # Actualizar estadísticos mediante la cadena de responsabilidad
        self.caracteristicas_sesion_actual = self._generador_audio.generar_estadistica(cancion)

    # ── Generación de recomendación ───────────────────────────────────────────

    def generar_recomendacion(self) -> dict[str, ElementoCatalogoMusical]:
        """Delega la búsqueda al generador de recomendaciones configurado."""
        if self._generador_recomendacion is None:
            raise RuntimeError("Debe llamar a configurar_recomendador antes de generar recomendaciones.")
        if not self.caracteristicas_sesion_actual:
            raise RuntimeError("El usuario no ha escuchado ninguna canción todavía.")
        return self._generador_recomendacion.recomendar(self.caracteristicas_sesion_actual)

    def __repr__(self) -> str:
        return f"SistemaRecomendacion(usuario={self.usuario_id!r})"


# ─────────────────────────────────────────────
# GENERACIÓN DE DATOS ALEATORIOS
# ─────────────────────────────────────────────

def _rand_dict(claves: list[str]) -> dict[str, float]:
    """Genera un diccionario de características con valores float aleatorios [0, 1]."""
    return {k: round(random.uniform(0, 1), 3) for k in claves}


def crear_catalogo_aleatorio(n_canciones: int = 30,
                              n_artistas: int = 5,
                              n_playlists: int = 5) -> CatalogoMusical:
    """Puebla un catálogo con datos aleatorios."""
    claves_audio = ["ritmo", "tono", "escala"]
    claves_sent = ["felicidad", "bailabilidad", "energia"]
    generos = list(GeneroMusical)
    fecha_base = date(1990, 1, 1)

    catalogo = CatalogoMusical()

    # Canciones
    for i in range(n_canciones):
        cancion = Cancion(
            id_=f"C{i:03d}",
            titulo=f"Cancion_{chr(65 + i % 26)}{i}",
            genero_musical=random.choice(generos),
            duracion=random.randint(120, 360),
            caracteristicas_musicales=_rand_dict(claves_audio),
            caracteristicas_sentimentales=_rand_dict(claves_sent),
            fecha_creacion=date(
                random.randint(1990, 2024),
                random.randint(1, 12),
                random.randint(1, 28)
            )
        )
        catalogo.canciones.append(cancion)

    # Artistas (cada uno con un subconjunto de canciones)
    for i in range(n_artistas):
        canciones_artista = random.sample(catalogo.canciones, k=min(5, n_canciones))
        artista = Artista(
            id_=f"A{i:03d}",
            nombre=f"Artista_{chr(65 + i)}",
            genero_musical=random.choice(generos),
            canciones=canciones_artista,
            fecha_nacimiento=date(
                random.randint(1960, 2000),
                random.randint(1, 12),
                random.randint(1, 28)
            )
        )
        catalogo.artistas.append(artista)

    # Playlists
    for i in range(n_playlists):
        canciones_pl = random.sample(catalogo.canciones, k=min(6, n_canciones))
        playlist = Playlist(
            id_=f"P{i:03d}",
            titulo=f"Playlist_{chr(65 + i)}",
            canciones=canciones_pl,
            fecha_creacion=date(
                random.randint(2010, 2024),
                random.randint(1, 12),
                random.randint(1, 28)
            )
        )
        catalogo.playlists.append(playlist)

    return catalogo


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

async def main():
    print("=" * 60)
    print("  SISTEMA DE RECOMENDACIÓN MUSICAL")
    print("=" * 60)

    # Crear catálogo
    catalogo = crear_catalogo_aleatorio(n_canciones=50, n_artistas=8, n_playlists=8)
    print(f"\nCatálogo generado: {catalogo}\n")

    # ── Demo 1: Singleton ────────────────────────────────────────
    print("── Demo Singleton ──")
    sistema_u1_a = SistemaRecomendacion("usuario_001")
    sistema_u1_b = SistemaRecomendacion("usuario_001")
    sistema_u2   = SistemaRecomendacion("usuario_002")
    print(f"sistema_u1_a is sistema_u1_b → {sistema_u1_a is sistema_u1_b}")  # True
    print(f"sistema_u1_a is sistema_u2   → {sistema_u1_a is sistema_u2}\n")  # False

    # ── Demo 2: Configurar y escuchar canciones ──────────────────
    print("── Demo Escucha + Estadísticos (Chain of Responsibility) ──")
    sistema = SistemaRecomendacion("usuario_demo")
    sistema.configurar_recomendador(
        catalogo=catalogo,
        target_element="cancion+artista+playlist",
        estrategia="aleatoria"
    )

    # Simular escucha de 5 canciones de forma asíncrona
    ids_escuchados = [c.id for c in random.sample(catalogo.canciones, 5)]
    for cid in ids_escuchados:
        await sistema.escuchar_cancion(cid)
        print(f"  Canción escuchada: {cid}")

    print(f"\n  Estadísticos de sesión actualizados ({len(sistema.caracteristicas_sesion_actual)} métricas).")

    # ── Demo 3: Generar recomendación ────────────────────────────
    print("\n── Demo Recomendación (Decorator + Strategy) ──")
    try:
        recomendacion = sistema.generar_recomendacion()
        for tipo, elemento in recomendacion.items():
            print(f"  Recomendación [{tipo}]: {elemento}")
    except SinRecomendacionError as e:
        print(f"  Sin recomendación: {e}")

    # ── Demo 4: Cambiar estrategia a Temporal ────────────────────
    print("\n── Demo Estrategia Temporal ──")
    sistema.configurar_recomendador(
        catalogo=catalogo,
        target_element="cancion+playlist",
        estrategia="temporal"
    )
    try:
        recomendacion = sistema.generar_recomendacion()
        for tipo, elemento in recomendacion.items():
            print(f"  Recomendación [{tipo}]: {elemento}")
    except SinRecomendacionError as e:
        print(f"  Sin recomendación: {e}")

    # ── Demo 5: Cambiar estrategia a Alfabética ──────────────────
    print("\n── Demo Estrategia Alfabética ──")
    sistema.configurar_recomendador(
        catalogo=catalogo,
        target_element="cancion",
        estrategia="alfabetica"
    )
    try:
        recomendacion = sistema.generar_recomendacion()
        for tipo, elemento in recomendacion.items():
            print(f"  Recomendación [{tipo}]: {elemento}")
    except SinRecomendacionError as e:
        print(f"  Sin recomendación: {e}")

    # ── Demo 6: Excepción canción no encontrada ──────────────────
    print("\n── Demo Excepción ──")
    try:
        await sistema.escuchar_cancion("ID_INEXISTENTE")
    except CancionNoEncontradaError as e:
        print(f"  CancionNoEncontradaError capturada: {e}")

    # ── Demo 7: Excepción estrategia inválida ────────────────────
    try:
        sistema.configurar_recomendador(catalogo, "cancion", "desconocida")
    except EstrategiaInvalidaError as e:
        print(f"  EstrategiaInvalidaError capturada: {e}")

    print("\n✓ Ejecución completada correctamente.")


if __name__ == "__main__":
    asyncio.run(main())
