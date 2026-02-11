import sys
import os

# --- BLOQUE DE CONFIGURACIÓN DE RUTA ---
# Esto permite encontrar la carpeta 'utils' aunque ejecutes este archivo
# directamente desde dentro de 'modelos'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# ---------------------------------------

from abc import ABC, abstractmethod
from utils.excepciones import ListaVaciaError


class RecursoMultimedia(ABC):
    """
    Clase Abstracta (Padre) que define la estructura básica de cualquier
    contenido reproducible en Spotipy (Canciones, Playlists, Albumes).
    """

    def __init__(self, titulo: str, img_portada: str, duracion: float = 0.0):
        # Atributos Protegidos (#) según el UML
        self._titulo = titulo
        self._imagen_portada = img_portada
        self._duracion = duracion  # Duración en segundos

    @property
    def titulo(self):
        # Getter publico para acceder al titulo.
        return self._titulo

    @property
    def duracion(self):
        # Getter publico para duración.
        return self._duracion

    @property
    def img_portada(self):
        # Getter publico para Imagen de Portada.
        return self._imagen_portada

    @abstractmethod
    def reproducir(self):
        """
        Método abstracto (+).
        Obliga a todas las clases hijas a definir SU propia forma de reproducirse.
        """
        pass

    def mostrar_detalle(self):
        """Método concreto (+) compartido por todos los hijos."""
        print(f"--- Info: {self._titulo} ({self._duracion} seg) ---")


class Cancion(RecursoMultimedia):
    """
    Clase Canción la unidad basica de reproducción, y contiene la ruta del archivo que usa el reproductor.
    """

    def __init__(
        self,
        titulo: str,
        artista: str,
        album: str,
        genero: str,
        ruta_archivo: str,
        duracion: float = 0,
        img_portada: str = "default.jpg",
    ):
        # Constructor de la clase padre.
        super().__init__(titulo, img_portada, duracion)
        # Atributos privados (-) propios de Cancion
        self.__artista = artista
        self.__album = album
        self.__genero = genero
        self.__ruta_archivo = ruta_archivo

    def __str__(self):
        cadena = f"{self.titulo}"
        return cadena

    def __repr__(self):
        cadena = f"{self.titulo}"
        return cadena

    # Getter de los atributos encapsulados.
    @property
    def artista(self):
        return self.__artista

    @property
    def album(self):
        return self.__album

    @property
    def genero(self):
        return self.__genero

    @property
    def ruta_archivo(self):
        return self.__ruta_archivo

    # Poliformismos para metodo reproducir.
    def reproducir(self):
        """
        Implementación concreta del método abstracto.
        Devuelve la ruta del archivo para que el motor de audio la use.
        """
        print(f"   🎵 Preparando sencillo: '{self.titulo}' de {self.__artista}...")
        return self.__ruta_archivo


class Playlist(RecursoMultimedia):
    """
    Clase Playlist,  colección mutable de canciones y es creada por el cliente,
    administrador y modificada por los mismos.
    """
    def __init__(self, titulo, descripcion : str, img_portada : str = "playlist.jpg"):
        # Constructor de la clase padre, se inicia con duración cero.
        super().__init__(titulo, img_portada, duracion=0)

    def __init__(
        self, titulo, img_portada, duracion, descripcion: str, canciones: list = []
    ):
        # Constructor de la clase padre.
        super().__init__(titulo, img_portada, duracion)
        # Atributos privados (-) propios de Playlist
        self.__descripcion = descripcion
        self.__canciones = [] # Lista Vacia.

    # Getter de los atributos encapsulados.
    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def canciones(self):
        return self.__canciones

    def agregar_cancion(self, cancion: Cancion):
        if isinstance(cancion, Cancion):
            self.__canciones.append(cancion)
            self._duracion += cancion.duracion
            print(f"[+] {cancion.titulo} agregada a {self.titulo}")

    def eliminar_cancion(self, cancion: Cancion):
        if cancion in self.__canciones:
            self.__canciones.remove(cancion)
            self._duracion -= cancion.duracion
            print(f"[-] {cancion.titulo} eliminada de {self.titulo}")

    # Poliformismos para metodo reproducir.
    def reproducir(self):
        """
        Versión de reproducir de Playlist.
        No retorna una ruta, sino la LISTA COMPLETA de objetos cancion, para que el REPRODUCTOR sepa que debe encolarlas todas.
        """
        if not self.__canciones:
            raise ListaVaciaError(f"La playlist '{self.titulo}' no tiene canciones.")

        print(
            f"   📂 Cargando Playlist: {self.titulo} ({len(self.__canciones)} pistas)"
        )
        # Retornamos la lista completa para que el controlador la gestione
        return self.__canciones


class Album(RecursoMultimedia):
    """
    Colección estática de canciones (lanzamiento oficial del artista).
    """
    def __init__(self, titulo,artista,año,canciones,img_portada = "album.jpg"):
        #Calculamos la duración total sumando las canciones al nacer.
        duracion_total=sum(c.duracion for c in canciones)
        super().__init__(titulo,img_portada,duracion_total)

    def __init__(self, titulo, artista, año, canciones, img_portada):
        # Calculamos la duración total sumando las canciones al nacer.
        duracion_total = sum(c.duracion for c in canciones)
        super().__init__(titulo, img_portada, duracion_total)
        self.__artista = artista
        self.__año = año
        self.__canciones = canciones

    @property
    def artista(self):
        return self.__artista

    # Poliformismos para metodo reproducir.
    def reproducir(self):
        """
        Versión de reproducir de Album.
        Basicamente hace lo mismo que la de Playlist, manda la lista de canciones al reproductor.
        """
        if not self.__canciones:
            raise ListaVaciaError(f"El Álbum '{self.titulo}' esta vacío (Error de datos).")
        
        print(f"   💿 Poniendo el vinilo: {self.titulo} - {self.__artista} ({self.__año})")
        return self.__canciones

# --- ZONA DE PRUEBAS (Al final del archivo) ---
if __name__ == "__main__":
    try:
        # 1. Creamos una canción falsa (sin archivo real por ahora)
        c1 = Cancion("Billie Jean", "Michael Jackson", "Thriller", "Pop", "ruta/falsa/c1.mp3", duracion=294)
        c2 = Cancion("Beat It", "Michael Jackson", "Thriller", "Rock", "ruta/falsa/c2.mp3", duracion=258)
        
        # 2. Probamos la canción
        print(f"Probando Canción: {c1.titulo}")
        c1.reproducir()
        
        # 3. Creamos un Album con esas canciones
        mi_album = Album("Thriller", "Michael Jackson", 1982, [c1, c2])
        print(f"\nProbando Álbum: {mi_album.titulo} (Duración: {mi_album.duracion} seg)")
        mi_album.reproducir()

        # 4. Creamos una Playlist y agregamos canciones
        mi_playlist = Playlist("Gym Motivation", "Para entrenar duro")
        mi_playlist.agregar_cancion(c2)
        print(f"\nProbando Playlist: {mi_playlist.titulo}")
        mi_playlist.reproducir()
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
