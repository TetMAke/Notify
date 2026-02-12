import sys
import os

# --- CONFIGURACIÓN DE RUTA ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# -----------------------------

from abc import ABC, abstractmethod
from modelos.multimedia import Playlist, Cancion
from utils.excepciones import ContrasenaIncorrectaError, PermisoDenegadoError


class Usuario(ABC):
    """
    Clase base para cualquier persona que accede al sistema.
    Maneja credenciales y datos básicos.
    """

    def __init__(self, nombre, correo, contraseña):
        self._nombre = nombre
        self._correo = correo
        self.__contraseña = contraseña  # Privado: Nadie debe verla
        self.bloqueado = False

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    def verificar_contrasena(self, intento):
        """Valida login y ESTADO de la cuenta."""
        if self.bloqueado:
            # Si está bloqueado, lanzamos error INMEDIATAMENTE
            raise PermisoDenegadoError(
                f"🚫 Tu cuenta ({self._correo}) ha sido SUSPENDIDA por un Administrador."
            )

        if intento == self.__contraseña:
            return True
        else:
            raise ContrasenaIncorrectaError(f"Contraseña inválida para {self._correo}")

    @abstractmethod
    def mostrar_menu_acciones(self):
        """Cada tipo de usuario verá opciones diferentes."""
        pass


class Cliente(Usuario):
    """
    Usuario estándar que consume contenido.
    """

    def __init__(self, nombre, correo, contraseña):
        super().__init__(nombre, correo, contraseña)
        self.mis_playlists = []  # Lista de objetos Playlist

    def crear_playlist(self, titulo, descripcion):
        """Crea una nueva playlist y la guarda en su perfil."""
        nueva_lista = Playlist(titulo, descripcion)
        self.mis_playlists.append(nueva_lista)
        print(f"✅ Playlist '{titulo}' creada exitosamente.")
        return nueva_lista

    def mostrar_menu_acciones(self):
        print(f"\n--- Panel de Cliente: {self.nombre} ---")
        print("1. Reproducir Música")
        print("2. Mis Playlists")
        print("3. Crear Playlist")
        print("4. Salir")


class Administrador(Usuario):
    """
    Usuario con permisos elevados para gestión.
    """

    def __init__(self, nombre, correo, contraseña, nivel_acceso=1):
        super().__init__(nombre, correo, contraseña)
        self.nivel_acceso = nivel_acceso

    def bloquear_usuario(self, usuario):
        """Cambia el estado del usuario a bloqueado."""
        if isinstance(usuario, Administrador):
            print(
                "❌ ERROR: No puedes bloquear a otro Administrador (Inmunidad Diplomática)."
            )
            return False

        if not usuario.bloqueado:
            usuario.bloqueado = True
            print(
                f"🚫 ¡BANEADO! El usuario {usuario.nombre} ha sido bloqueado del sistema."
            )
            return True
        else:
            usuario.bloqueado = False
            print(
                f"✅ ¡DESBANEADO! El usuario {usuario.nombre} ha sido desbloqueado del sistema."
            )
            return True

    def mostrar_menu_acciones(self):
        print(f"\n--- Panel de ADMINISTRADOR: {self.nombre} ---")
        print("1. Gestionar Catálogo Musical")
        print("2. Bloquear Usuarios")
        print("3. Estadísticas del Sistema")
        print("4. Salir")


# --- ZONA DE PRUEBAS ---
if __name__ == "__main__":
    try:
        print("--- TEST DE USUARIOS ---")

        # 1. Crear un Cliente
        cliente1 = Cliente("Carlos", "carlos@gmail.com", "1234")

        # 2. Probar contraseña
        print(f"Intentando login con '1234': {cliente1.verificar_contrasena('1234')}")

        try:
            cliente1.verificar_contrasena("0000")
        except ContrasenaIncorrectaError as e:
            print(f"Error esperado capturado: {e}")

        # 3. Cliente crea playlist
        pl_rock = cliente1.crear_playlist("Rock Clásico", "Mis favoritas")

        # 4. Crear Admin
        admin = Administrador("Jefa", "admin@spotipy.com", "admin123")

        # 5. Admin bloquea a cliente
        admin.bloquear_usuario(cliente1)

        print("\n--- TEST FINALIZADO ---")

    except Exception as e:
        print(f"Error grave: {e}")
