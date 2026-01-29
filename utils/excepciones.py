class SpotipyError(Exception):
    """
    Clase base (Padre) para todas las excepciones del proyecto Spotipy.
    Hereda de la clase nativa Exception de Python.
    """

    def __init__(self, mensaje: str = "Ocurrio un error en la aplicación Spotipy"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# --- Excepciones de Usuario ---


class UsuarioNoEncontradoError(SpotipyError):
    """Excepción lanzada cuando no se encuentra un usuario en la búsqueda."""

    def __init__(self, mensaje="El usuario buscado no existe en el sistema"):
        super().__init__(mensaje)


class ContrasenaIncorrectaError(SpotipyError):
    """Excepción lanzada cuando la contraseña no coincide."""

    def __init__(self, mensaje="Contraseña incorrecta"):
        super().__init__(mensaje)


class UsuarioYaRegistradoError(SpotipyError):
    """Excepción lanzada al intentar registrar un email ya existente."""

    def __init__(self, mensaje="El usuario ya se encuentra registrado"):
        super().__init__(mensaje)


class PermisoDenegadoError(SpotipyError):
    """Excepción lanzada cuando un usuario intenta realizar una acción no permitida para su rol."""

    def __init__(self, mensaje="No tienes permisos para realizar esta acción"):
        super().__init__(mensaje)


# --- Excepciones de Multimedia ---


class CancionNoEncontradaError(SpotipyError):
    """Excepción lanzada cuando una canción no existe en el catálogo."""

    def __init__(self, mensaje="La canción solicitada no se encuentra disponible"):
        super().__init__(mensaje)


class PlaylistNoEncontradaError(SpotipyError):
    """Excepción lanzada cuando no se encuentra una playlist específica."""

    def __init__(self, mensaje="La playlist solicitada no existe"):
        super().__init__(mensaje)


class ArchivoAudioNoEncontradoError(SpotipyError):
    """Excepción crítica: El objeto Cancion existe, pero el archivo .mp3 no está en la carpeta assets."""

    def __init__(
        self,
        mensaje="El archivo de audio físico no fue encontrado en la ruta especificada",
    ):
        super().__init__(mensaje)


class ListaVaciaError(SpotipyError):
    """Excepción lanzada al intentar reproducir una lista sin canciones."""

    def __init__(self, mensaje="La lista de reproducción está vacía"):
        super().__init__(mensaje)


# --- Excepciones de Control ---


class OpcionInvalidaError(SpotipyError):
    """Excepción lanzada cuando el usuario ingresa una opción de menú no válida."""

    def __init__(self, mensaje="La opción ingresada no es válida"):
        super().__init__(mensaje)


if __name__ == "__main__":
    try:
        raise SpotipyError("Falló el login")
    except SpotipyError as e:
        # Para leer el mensaje tendrías que hacer esto:
        print(e)  # ¡Es poco intuitivo y difícil de recordar!
