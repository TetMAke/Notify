import sys
import os
import time

# Importaciones de nuestros módulos
from modelos.usuario import Cliente, Administrador
from modelos.multimedia import Cancion, Playlist, Album
from servicios.reproductor import Reproductor
from utils.excepciones import (
    SpotipyError,
    UsuarioNoEncontradoError,
    ContrasenaIncorrectaError,
)

# --- BASE DE DATOS SIMULADA (RAM) ---
usuarios_db = []
catalogo_musica = []
reproductor = Reproductor()  # Instancia única del motor de audio


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Mac/Linux
        os.system("clear")


def inicializar_datos():
    """Crea datos de prueba para que el sistema no esté vacío."""
    limpiar_pantalla()
    print("🔄 Inicializando sistema Spotipy...")
    time.sleep(1)  # Pequeña pausa dramática

    # 1. Crear Canciones (Simuladas)
    c1 = Cancion(
        "Billie Jean",
        "Michael Jackson",
        "Thriller",
        "Pop",
        "assets/01 Enter Pharloom.mp3",
        294,
    )
    c2 = Cancion(
        "Bohemian Rhapsody",
        "Queen",
        "A Night at the Opera",
        "Rock",
        "assets/musica/bohemian.mp3",
        354,
    )
    c3 = Cancion(
        "Shape of You", "Ed Sheeran", "Divide", "Pop", "assets/musica/shape.mp3", 233
    )

    catalogo_musica.extend([c1, c2, c3])

    # 2. Crear Usuarios
    # Admin (Clave: admin123)
    admin = Administrador("Super Admin", "admin@spotipy.com", "admin123")

    # Cliente (Clave: 1234)
    cliente = Cliente("Juan Perez", "juan@gmail.com", "1234")
    # Le regalamos una playlist al cliente
    pl_rock = cliente.crear_playlist("Mis Favoritas", "Rock y Pop")
    pl_rock.agregar_cancion(c2)
    pl_rock.agregar_cancion(c3)

    usuarios_db.extend([admin, cliente])


def sistema_login():
    """Maneja la autenticación del usuario."""
    while True:
        limpiar_pantalla()
        print("=== 🔐 BIENVENIDO A SPOTIPY ===")
        print("-------------------------------")
        email = input("📧 Correo: ")
        password = input("🔑 Contraseña: ")

        try:
            # 1. Buscar usuario
            usuario_encontrado = None
            for u in usuarios_db:
                if u.correo == email:
                    usuario_encontrado = u
                    break

            if not usuario_encontrado:
                raise UsuarioNoEncontradoError(f"No existe cuenta con {email}")

            # 2. Verificar password
            usuario_encontrado.verificar_contrasena(password)

            print(f"\n👋 ¡Hola de nuevo, {usuario_encontrado.nombre}!")
            time.sleep(1.5)  # Pausa para ver el saludo
            return usuario_encontrado

        except SpotipyError as e:
            print(f"\n❌ Error de acceso: {e.mensaje}")
            input("   (Presiona Enter para intentar de nuevo...)")


def menu_reproduccion():
    """Sub-menú para controlar la música que suena."""
    while True:
        limpiar_pantalla()  # Refrescamos la interfaz del reproductor
        print("\n--- 🎵 REPRODUCTOR SPOTIPY ---")

        if reproductor.cola:
            actual = reproductor.cola[reproductor.indice_actual]
            # Estado visual
            estado = "▶️  SONANDO" if reproductor.reproduciendo else "⏸️  PAUSADO"

            # Decoración visual simple
            print(f"┌──────────────────────────────────────┐")
            print(f"│ {estado.center(37)} │")
            print(f"│                                      │")
            print(f"│ 🎵 {actual.titulo[:32].center(33)} │")
            print(f"│ 👤 {actual.artista[:32].center(33)} │")
            print(f"└──────────────────────────────────────┘")
        else:
            print("   (Nada reproduciéndose)")

        print("\n[P] Play/Pause | [S]iguiente | [A]nterior | [V]olumen | [X] Salir")
        opcion = input(">> Opción: ").upper()

        if opcion == "P":
            # --- LOGICA TOGGLE (INTERRUPTOR) ---
            if reproductor.reproduciendo:
                reproductor.pausar()
            else:
                reproductor.despausar()
            # No ponemos pausa aquí para que refresque rápido la pantalla

        elif opcion == "S":
            reproductor.siguiente()
        elif opcion == "A":
            reproductor.anterior()
        elif opcion == "V":
            try:
                vol = float(input("\nNivel (0.0 a 1.0): "))
                reproductor.cambiar_volumen(vol)
                time.sleep(1)  # Breve pausa para leer el volumen
            except ValueError:
                print("❌ Ingresa un número válido.")
                time.sleep(1)
        elif opcion == "X":
            break
        else:
            print("Opción no válida.")
            time.sleep(0.5)


def menu_principal(usuario):
    """Bucle principal de la aplicación."""
    while True:
        limpiar_pantalla()
        # Polimorfismo: Cada usuario muestra SU menú
        usuario.mostrar_menu_acciones()

        opcion = input("\n>> Selecciona una opción: ")

        try:
            if isinstance(usuario, Cliente):
                if opcion == "1":  # Reproducir del catálogo
                    limpiar_pantalla()
                    print("\n--- 🌎 CATÁLOGO GLOBAL ---")
                    for i, cancion in enumerate(catalogo_musica):
                        print(f"{i+1}. {cancion.titulo} - {cancion.artista}")
                    print("--------------------------")

                    entrada = input("Número de canción a reproducir (0 para salir): ")
                    if entrada.isdigit():
                        idx = int(entrada) - 1
                        if 0 <= idx < len(catalogo_musica):
                            reproductor.cargar_origen(catalogo_musica[idx])
                            menu_reproduccion()  # Entramos al control

                elif opcion == "2":  # Ver Playlists
                    limpiar_pantalla()
                    print("\n--- 📂 MIS PLAYLISTS ---")
                    if not usuario.mis_playlists:
                        print("No tienes playlists creadas.")
                        input("\nPresiona Enter para volver...")
                    else:
                        for i, pl in enumerate(usuario.mis_playlists):
                            print(f"{i+1}. {pl.titulo} ({len(pl.canciones)} canciones)")

                        entrada = input(
                            "\nElige playlist para reproducir (0 para salir): "
                        )
                        if entrada.isdigit():
                            idx = int(entrada) - 1
                            if 0 <= idx < len(usuario.mis_playlists):
                                reproductor.cargar_origen(usuario.mis_playlists[idx])
                                menu_reproduccion()

                elif opcion == "3":  # Crear Playlist
                    limpiar_pantalla()
                    print("--- ✨ NUEVA PLAYLIST ---")
                    titulo = input("Nombre de la playlist: ")
                    desc = input("Descripción: ")
                    usuario.crear_playlist(titulo, desc)
                    input("\n✅ Playlist creada. Presiona Enter para continuar...")

                elif opcion == "4":  # Salir
                    print("\nCerrando sesión...")
                    reproductor.detener()
                    time.sleep(1)
                    break

            elif isinstance(usuario, Administrador):
                if opcion == "1":
                    print(f"\nCatálogo actual: {len(catalogo_musica)} canciones.")
                    input("Presiona Enter...")

                elif opcion == "2":  # --- ZONA DE BLOQUEO ---
                    limpiar_pantalla()
                    print("\n--- ⚖️ TRIBUNAL DE ADMINISTRACIÓN ---")
                    print("Selecciona el usuario a bloquear permanentemente:")

                    # Filtramos la lista para no mostrar al propio admin
                    # (Creamos una lista temporal de candidatos)
                    candidatos = [
                        u for u in usuarios_db if not isinstance(u, Administrador)
                    ]

                    if not candidatos:
                        print("   (No hay clientes registrados para bloquear)")
                    else:
                        for i, user in enumerate(candidatos):
                            estado = (
                                "🚫 (Ya Bloqueado)" if user.bloqueado else "✅ (Activo)"
                            )
                            print(f"{i+1}. {user.nombre} | {user.correo} {estado}")

                        print("---------------------------------------")
                        entrada = input(
                            "Número de usuario a bloquear/desbloquear (0 cancelar): "
                        )

                        if entrada.isdigit():
                            idx = int(entrada) - 1
                            if 0 <= idx < len(candidatos):
                                usuario_objetivo = candidatos[idx]
                                # LLAMADA AL PODER DEL ADMIN
                                exito = usuario.bloquear_usuario(usuario_objetivo)
                                if exito:
                                    # Efecto dramático
                                    time.sleep(1)
                                    print(
                                        "   Actualizando base de datos de seguridad..."
                                    )
                            else:
                                print("Opción cancelada.")
                        else:
                            print("Entrada inválida.")

                    input("\nPresiona Enter para volver...")

                elif opcion == "4":
                    break

            else:
                print("Opción no reconocida.")
                time.sleep(1)

        except ValueError:
            print("\n❌ Error: Debes ingresar un número válido.")
            input("Presiona Enter...")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presiona Enter...")


if __name__ == "__main__":
    # 1. Cargar datos
    inicializar_datos()

    # 2. Loop infinito del programa
    while True:
        try:
            # A. Login
            usuario_activo = sistema_login()

            # B. Menú Principal
            menu_principal(usuario_activo)

        except KeyboardInterrupt:
            print("\n\nApagando Spotipy... ¡Adiós!")
            break
