# import pygame
# import time

# # 1. Inicializar solo el mixer, no pygame completo
# pygame.mixer.init()

# # 2. Cargar y reproducir música
# pygame.mixer.music.load("assets/01 Enter Pharloom.mp3")
# pygame.mixer.music.play()

# # 3. Registrar el tiempo de inicio
# start_time = pygame.time.get_ticks()

# print("Reproduciendo música...")

# # Bucle de monitoreo
# running = True
# while running:
#     # 4. Calcular tiempo transcurrido
#     tiempo_actual = pygame.time.get_ticks()
#     segundos_transcurridos = (tiempo_actual - start_time) / 1000

#     print(f"Tiempo: {segundos_transcurridos:.2f} s", end="\r")

#     # Salir si la música termina
#     if not pygame.mixer.music.get_busy():
#         print("\nLa música ha terminado.")
#         running = False

#     # Pequeña pausa para no saturar la CPU
#     pygame.time.wait(100)


# # --- INTENTO DE IMPORTAR MUTAGEN ---
# try:
#     from mutagen.easyid3 import EasyID3
#     from mutagen.mp3 import MP3

#     MUTAGEN_DISPONIBLE = True
# except ImportError:
#     MUTAGEN_DISPONIBLE = False
#     print("⚠️ 'mutagen' no instalado. El escáner usará datos básicos.")


# def escanear_carpeta(ruta_directorio):
#     """
#     Escanea una carpeta en busca de archivos .mp3, extrae sus metadatos
#     y los convierte en objetos Cancion para el catálogo.
#     """
#     if not os.path.isdir(ruta_directorio):
#         print(f"❌ Error: La carpeta '{ruta_directorio}' no existe.")
#         return 0

#     canciones_encontradas = 0

#     # os.listdir lee todos los archivos dentro de la carpeta
#     for archivo in os.listdir(ruta_directorio):
#         if archivo.lower().endswith(".mp3"):
#             ruta_completa = os.path.join(ruta_directorio, archivo)

#             # Valores por defecto (Fallback)
#             titulo = archivo[:-4]  # Quitamos el ".mp3" del nombre
#             artista = "Desconocido"
#             album = "Desconocido"
#             genero = "Desconocido"
#             duracion = 0.0

#             # Si Mutagen está instalado, extraemos la magia
#             if MUTAGEN_DISPONIBLE:
#                 try:
#                     audio = MP3(ruta_completa, ID3=EasyID3)
#                     # get() devuelve una lista, tomamos el primer elemento [0]
#                     titulo = audio.get("title", [titulo])[0] # type: ignore
#                     artista = audio.get("artist", [artista])[0] # type: ignore
#                     album = audio.get("album", [album])[0] # type: ignore
#                     genero = audio.get("genre", [genero])[0] # type: ignore
#                     duracion = round(audio.info.length, 2)
#                 except Exception as e:
#                     print(f"   ⚠️ No se pudieron leer metadatos de {archivo}")

#             # Creamos el objeto y lo metemos al catálogo global
#             nueva_cancion = Cancion(
#                 titulo, artista, album, genero, ruta_completa, duracion
#             )
#             catalogo_musica.append(nueva_cancion)
#             canciones_encontradas += 1

#     return canciones_encontradas
