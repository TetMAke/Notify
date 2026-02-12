import pygame
import time

# 1. Inicializar solo el mixer, no pygame completo
pygame.mixer.init()

# 2. Cargar y reproducir música
pygame.mixer.music.load("assets/01 Enter Pharloom.mp3")
pygame.mixer.music.play()

# 3. Registrar el tiempo de inicio
start_time = pygame.time.get_ticks()

print("Reproduciendo música...")

# Bucle de monitoreo
running = True
while running:
    # 4. Calcular tiempo transcurrido
    tiempo_actual = pygame.time.get_ticks()
    segundos_transcurridos = (tiempo_actual - start_time) / 1000

    print(f"Tiempo: {segundos_transcurridos:.2f} s", end="\r")

    # Salir si la música termina
    if not pygame.mixer.music.get_busy():
        print("\nLa música ha terminado.")
        running = False

    # Pequeña pausa para no saturar la CPU
    pygame.time.wait(100)
