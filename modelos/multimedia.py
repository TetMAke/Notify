from abc import ABC, abstractmethod


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
        img_portada: str,
        artista: str,
        album: str,
        genero: str,
        ruta_archivo: str,
        duracion: float = 0,
    ):
        # Constructor de la clase padre.
        super().__init__(titulo, img_portada, duracion)
        # Atributos privados (-) propios de Cancion
        self.__artista = artista
        self.__album = album
        self.__genero = genero
        self.__ruta_archivo = ruta_archivo

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
