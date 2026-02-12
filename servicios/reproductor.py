import sys
import os
import time

# --- CONFIGURACIÓN DE RUTA ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# -----------------------------

# Intentamos importar pygame. Si falla, avisamos pero no rompemos el programa inmediatamente
try:
    import pygame

    PYGAME_DISPONIBLE = True
except ImportError:
    PYGAME_DISPONIBLE = False
    print("⚠️ ADVERTENCIA: 'pygame-ce' no está instalado. El audio será 100% simulado.")

from modelos.multimedia import Cancion, Playlist, Album
from utils.excepciones import ListaVaciaError


class Reproductor:
    """
    Fachada (Facade) para controlar la reproducción de audio.
    Gestiona la cola de canciones y la interacción con la librería Pygame.
    """

    def __init__(self):
        self.cola = []  # Lista de objetos Cancion
        self.indice_actual = 0  # Cuál canción de la cola está sonando
        self.reproduciendo = False  # Estado del reproductor.
        global start_time

        # Inicializar motor de audio si es posible
        if PYGAME_DISPONIBLE:
            pygame.mixer.init()
            self.volumen = 0.5
            pygame.mixer.music.set_volume(self.volumen)
        else:
            self.volumen = 0.0

    def cargar_origen(self, recurso):
        """
        Recibe un objeto (Cancion, Playlist o Album) y prepara la cola.
        """
        self.detener()  # Limpiamos lo anterior
        self.cola = []
        self.indice_actual = 0

        # POLIMORFISMO: Detectamos qué nos mandaron
        if isinstance(recurso, Cancion):
            self.cola.append(recurso)
            print(f"💿 Reproductor: Cargado sencillo '{recurso.titulo}'")

        elif isinstance(recurso, (Playlist, Album)):
            # Usamos el método reproducir() de la clase para obtener la lista
            try:
                lista_canciones = recurso.reproducir()  # Esto devuelve la lista
                self.cola = lista_canciones
                print(
                    f"📚 Reproductor: Cargada lista '{recurso.titulo}' ({len(self.cola)} canciones)"
                )
            except ListaVaciaError as e:
                print(f"❌ Error: {e}")
                return

        # Iniciamos automáticamente
        if self.cola:
            self._reproducir_actual()

    def _reproducir_actual(self):
        """Método interno para procesar la canción actual de la cola."""
        if not self.cola:
            return

        cancion_actual = self.cola[self.indice_actual]
        ruta = cancion_actual.ruta_archivo

        print(f"\n▶️ REPRODUCIENDO: {cancion_actual.titulo} - {cancion_actual.artista}")

        # --- Lógica Híbrida ---
        # Guardamos el tiempo de inicio (para el modo simulación o fallback)
        self.start_time = time.time()

        if PYGAME_DISPONIBLE and os.path.exists(ruta):
            try:
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.play()
                self.reproduciendo = True
            except Exception as e:
                print(f"⚠️ Error técnico con Pygame: {e}. Pasando a modo simulación.")
                self.reproduciendo = True
        else:
            # Modo Simulación
            print(f"   (Modo Simulación: Archivo no encontrado o Pygame ausente)")
            print("   🎶 [Suena música imaginaria] 🎶")
            self.reproduciendo = True

    def pausar(self):
        if PYGAME_DISPONIBLE and self.reproduciendo:
            pygame.mixer.music.pause()
            self.reproduciendo = False
            print("⏸️ Pausado")
        else:
            print("⏸️ (Simulación) Pausado")

    def despausar(self):
        if PYGAME_DISPONIBLE and not self.reproduciendo:
            pygame.mixer.music.unpause()
            self.reproduciendo = True
            print("▶️ Reanudando")
        else:
            print("▶️ (Simulación) Reanudando")

    def detener(self):
        if PYGAME_DISPONIBLE:
            pygame.mixer.music.stop()
        self.reproduciendo = False
        print("⏹️ Detenido")

    def siguiente(self):
        """Pasa a la siguiente canción de la cola."""
        if self.indice_actual < len(self.cola) - 1:
            self.indice_actual += 1
            self._reproducir_actual()
        else:
            print("End of Playlist. Volviendo al inicio...")
            self.indice_actual = 0  # Loop
            self._reproducir_actual()

    def anterior(self):
        """
        Regresa a la canción anterior si han pasado menos de 5 segundos.
        Si han pasado más de 5 segundos, reinicia la canción actual.
        """
        segundos_transcurridos = 0

        # 1. Calcular cuánto tiempo lleva sonando
        if PYGAME_DISPONIBLE and pygame.mixer.music.get_busy():
            # get_pos devuelve milisegundos, dividimos por 1000
            segundos_transcurridos = pygame.mixer.music.get_pos() / 1000
        else:
            # Fallback para modo simulación: Usamos time.time()
            segundos_transcurridos = time.time() - self.start_time

        print(f"   (Tiempo transcurrido: {segundos_transcurridos:.1f} seg)")

        # 2. Lógica de decisión Spotify
        if segundos_transcurridos > 5:
            # CASO A: Ya avanzó mucho, reiniciamos la MISMA canción
            print("   ⏮️ +5 segundos: Reiniciando canción actual...")
            self._reproducir_actual()
        else:
            # CASO B: Lleva poco tiempo, intentamos ir atrás
            if self.indice_actual > 0:
                print("   ⏮️ Regresando al track anterior...")
                self.indice_actual -= 1
                self._reproducir_actual()
            else:
                print("   ⛔ Estás en la primera canción (Se reinicia).")
                self._reproducir_actual()

    def cambiar_volumen(self, nivel):
        """Nivel de 0.0 a 1.0"""
        if 0.0 <= nivel <= 1.0:
            self.volumen = nivel
            if PYGAME_DISPONIBLE:
                pygame.mixer.music.set_volume(self.volumen)
            print(f"🔊 Volumen ajustado a: {int(nivel*100)}%")
        else:
            print("⚠️ Volumen debe ser entre 0.0 y 1.0")


# --- ZONA DE PRUEBAS ---
if __name__ == "__main__":
    # Creamos datos dummy para probar sin necesitar archivos reales
    c1 = Cancion(
        "Enter Pharloom", "Artist A", "Alb 1", "Rock", "assets/01 Enter Pharloom.mp3"
    )
    c2 = Cancion("Moss Grotto", "Artist B", "Alb 1", "Pop", "assets/02 Moss Grotto.mp3")

    mi_playlist = Playlist("Mix Verano", "Test")
    mi_playlist.agregar_cancion(c1)
    mi_playlist.agregar_cancion(c2)

    dj = Reproductor()
    dj.cambiar_volumen(1)

    print("--- PRUEBA: Cargar Playlist ---")
    dj.cargar_origen(mi_playlist)

    # Simulamos interacción de usuario
    time.sleep(10)
    print("\n--- PRUEBA: Siguiente ---")
    dj.siguiente()
    # dj.siguiente()

    time.sleep(5)
    print("\n--- PRUEBA: Anterior ---")
    dj.anterior()

    time.sleep(60)
    print("\n--- PRUEBA: Stop ---")
    dj.detener()
