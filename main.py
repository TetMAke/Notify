import sys
import os
import time
import msvcrt

# Importaciones de nuestros módulos
from modelos.usuario import Cliente, Administrador
from modelos.multimedia import Cancion, Playlist, Album
from servicios.reproductor import Reproductor
from utils.excepciones import (
    NotifyError,
    UsuarioNoEncontradoError,
    ContrasenaIncorrectaError,
)

# --- INTENTO DE IMPORTAR MUTAGEN ---
try:
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3

    MUTAGEN_DISPONIBLE = True
except ImportError:
    MUTAGEN_DISPONIBLE = False
    print("⚠️ 'mutagen' no instalado. El escáner usará datos básicos.")


def escanear_carpeta(ruta_directorio):
    """
    Escanea recursivamente una carpeta y sus subcarpetas.
    Extrae metadatos, crea objetos Cancion y agrupa automáticamente en objetos Album.
    """
    if not os.path.isdir(ruta_directorio):
        print(f"❌ Error: La carpeta '{ruta_directorio}' no existe.")
        return 0, 0  # Ahora devolvemos dos valores: (canciones, albumes)

    canciones_encontradas = 0
    # Diccionario para agrupar canciones: {"Nombre del Album": {"artista": "X", "año": 2024, "canciones": [c1, c2]}}
    albumes_temp = {}

    # os.walk recorre la raíz y TODAS las subcarpetas mágicamente
    for raiz, subcarpetas, archivos in os.walk(ruta_directorio):
        for archivo in archivos:
            if archivo.lower().endswith(".mp3"):
                ruta_completa = os.path.join(raiz, archivo).replace("\\", "/")

                # Fallbacks (Valores por defecto si no hay metadatos)
                titulo = archivo[:-4]
                artista = "Desconocido"
                album_nombre = "Desconocido"
                genero = "Desconocido"
                duracion = 0.0
                año = 2024

                # Extraer metadatos reales con Mutagen
                if MUTAGEN_DISPONIBLE:
                    try:
                        audio = MP3(ruta_completa, ID3=EasyID3)
                        titulo = audio.get("title", [titulo])[0]  # type: ignore
                        artista = audio.get("artist", [artista])[0]  # type: ignore
                        album_nombre = audio.get("album", [album_nombre])[0]  # type: ignore
                        genero = audio.get("genre", [genero])[0]  # type: ignore
                        duracion = round(audio.info.length, 2)

                        # Intentamos sacar el año (A veces viene como fecha completa ej: 1982-11-30)
                        fecha = audio.get("date", [str(año)])[0]  # type: ignore
                        año = int(fecha[:4]) if fecha[:4].isdigit() else año
                    except Exception as e:
                        print(f"   ⚠️ Metadatos incompletos en {archivo}")

                # 1. Creamos la canción individual
                nueva_cancion = Cancion(
                    titulo, artista, album_nombre, genero, ruta_completa, duracion
                )
                catalogo_musica.append(nueva_cancion)
                canciones_encontradas += 1

                # 2. Agrupamos la canción para su Álbum (Solo si tiene un álbum real)
                if album_nombre and album_nombre.lower() != "desconocido":
                    if album_nombre not in albumes_temp:
                        albumes_temp[album_nombre] = {
                            "artista": artista,
                            "año": año,
                            "canciones": [],
                        }
                    albumes_temp[album_nombre]["canciones"].append(nueva_cancion)

    # 3. Construir los objetos Album
    albumes_creados = 0
    for nom_album, datos in albumes_temp.items():
        if len(datos["canciones"]) > 0:
            nuevo_album = Album(
                nom_album, datos["artista"], datos["año"], datos["canciones"]
            )
            # Añadimos el Álbum COMPLETO al catálogo global gracias al Polimorfismo
            catalogo_musica.append(nuevo_album)
            albumes_creados += 1

    return canciones_encontradas, albumes_creados


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
    print("🔄 Inicializando sistema Notify...")
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
        "assets/02 Moss Grotto.mp3",
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
        print("=== 🔐 BIENVENIDO A Notify ===")
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

        except NotifyError as e:
            print(f"\n❌ Error de acceso: {e.mensaje}")
            input("   (Presiona Enter para intentar de nuevo...)")


def menu_reproduccion():
    """Sub-menú para controlar la música que suena."""
    while True:
        limpiar_pantalla()  # Refrescamos la interfaz del reproductor
        print("\n--- 🎵 REPRODUCTOR NOTIFY ---")

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

        # --- BUCLE DE ESPERA ASÍNCRONA (Prueba Eliminar INPUT) ---
        # En lugar del input() que bloquea el sistema, revisamos rápidamente qué pasa usando msvcrt
        # opcion = input(">> Opción: ").upper()
        opcion = None
        # Nuevo estados de verificación para comparar con el estado del threads e identificar un cambio realizado por el vigilante y actualizar la pantalla.
        estado_original = reproductor.reproduciendo
        indice_original = reproductor.indice_actual

        while True:
            # 1. ¿El usuario presionó alguna tecla?
            if msvcrt.kbhit():
                # getch() captura la tecla instantáneamente sin presionar Enter
                tecla_cruda = msvcrt.getch()
                try:
                    opcion = tecla_cruda.decode("utf-8").upper()
                except UnicodeDecodeError:
                    opcion = ""  # Ignoramos teclas especiales como las flechas
                break  # Salimos del mini-bucle para ejecutar la acción

            # 2. ¿El vigilante de fondo cambió la canción o el estado?
            if (
                reproductor.indice_actual != indice_original
                or reproductor.reproduciendo != estado_original
            ):
                opcion = "REDIBUJAR_PANTALLA"
                break

            # Pausa microscópica para no sobrecargar el procesador de tu PC
            time.sleep(0.1)

        # --- EJECUCIÓN DE COMANDOS ---
        if opcion == "REDIBUJAR_PANTALLA":
            continue  # Simplemente vuelve a iniciar el while y dibuja la nueva canción

        elif opcion == "P":
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
            # Aquí sí usamos input normal porque necesitamos escribir números (ej. 0.5)
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


def gestionar_catalogo():
    while True:
        limpiar_pantalla()
        print(f"\n--- 🗂️ GESTIÓN DE CATÁLOGO ({len(catalogo_musica)} pistas) ---")
        print("1. Ver Catálogo Completo")
        print("2. Agregar Nueva Canción")
        print("3. Editar Canción")
        print("4. Eliminar Canción")
        print("5. Escanear Carpeta (Auto-Importar)")
        print("6. Volver al menú anterior")

        sub_opcion = input("\n>> Opción: ")

        if sub_opcion == "1":
            limpiar_pantalla()
            print("--- 🌎 CATÁLOGO GLOBAL ---")
            if not catalogo_musica:
                print("El catálogo está vacío.")
            else:
                for i, item in enumerate(catalogo_musica):
                    if isinstance(item, Album):
                        print(
                            f"{i+1}. 💿 [ÁLBUM] {item.titulo} - {item.artista} ({len(item._Album__canciones)} pistas)"  # type: ignore
                        )
                    else:
                        print(f"{i+1}. 🎵 [PISTA] {item.titulo} - {item.artista}")
            input("\nPresiona Enter para volver...")

        elif sub_opcion == "2":
            limpiar_pantalla()
            print("--- ➕ AGREGAR NUEVA CANCIÓN ---")
            print(
                "Ingresa los datos de la pista (o escribe 'X' en el título para cancelar):\n"
            )

            tit = input("🎵 Título: ")
            if tit.upper() == "X":
                continue  # Cancela y vuelve al sub-menú

            art = input("👤 Artista: ")
            alb = input("💿 Álbum: ")
            gen = input("🎸 Género: ")
            ruta = input("📂 Ruta del archivo (ej. assets/03_nueva.mp3): ")

            # Validación de seguridad para la duración (evita que el programa explote si escriben texto)
            try:
                dur = float(input("⏱️ Duración en segundos: "))
            except ValueError:
                print("   ⚠️ Duración inválida. Se asignará 0 segundos por defecto.")
                dur = 0.0

            # Creamos el objeto Canción y lo añadimos a la lista global
            nueva_cancion = Cancion(tit, art, alb, gen, ruta, dur)
            catalogo_musica.append(nueva_cancion)

            print(f"\n✅ ¡Éxito! '{tit}' se ha agregado al catálogo global.")
            time.sleep(1.5)

        elif sub_opcion == "3":
            limpiar_pantalla()
            print("--- ✏️ EDITAR CANCIÓN ---")
            if not catalogo_musica:
                print("El catálogo está vacío.")
                input("\nPresiona Enter para volver...")
                continue

            for i, c in enumerate(catalogo_musica):
                print(f"{i+1}. {c.titulo} - {c.artista}")

            entrada = input("\nNúmero de canción a editar (0 para cancelar): ")
            if entrada.isdigit():
                idx = int(entrada) - 1
                if 0 <= idx < len(catalogo_musica):
                    c_actual = catalogo_musica[idx]
                    print(
                        "\nDejar en blanco y presionar Enter mantiene el valor actual:"
                    )

                    # Usamos 'or' para mantener el valor viejo si el input está vacío
                    tit = input(f"🎵 Título ({c_actual.titulo}): ") or c_actual.titulo
                    art = (
                        input(f"👤 Artista ({c_actual.artista}): ") or c_actual.artista
                    )
                    alb = input(f"💿 Álbum ({c_actual.album}): ") or c_actual.album
                    gen = input(f"🎸 Género ({c_actual.genero}): ") or c_actual.genero
                    ruta = (
                        input(f"📂 Ruta ({c_actual.ruta_archivo}): ")
                        or c_actual.ruta_archivo
                    )

                    try:
                        dur_input = input(f"⏱️ Duración ({c_actual.duracion}): ")
                        dur = float(dur_input) if dur_input else c_actual.duracion
                    except ValueError:
                        dur = c_actual.duracion

                    # Reemplazamos el objeto en la lista
                    catalogo_musica[idx] = Cancion(tit, art, alb, gen, ruta, dur)
                    print(f"\n✅ Canción '{tit}' actualizada correctamente.")
                    time.sleep(1.5)

        elif sub_opcion == "4":
            limpiar_pantalla()
            print("--- 🗑️ ELIMINAR CANCIÓN ---")
            if not catalogo_musica:
                print("El catálogo está vacío.")
                input("\nPresiona Enter para volver...")
                continue

            for i, c in enumerate(catalogo_musica):
                print(f"{i+1}. {c.titulo} - {c.artista}")

            entrada = input("\nNúmero de canción a eliminar (0 para cancelar): ")
            if entrada.isdigit():
                idx = int(entrada) - 1
                if 0 <= idx < len(catalogo_musica):
                    # pop() saca el elemento de la lista y nos lo devuelve
                    eliminada = catalogo_musica.pop(idx)
                    print(
                        f"\n🗑️ La canción '{eliminada.titulo}' ha sido eliminada del catálogo."
                    )
                    time.sleep(1.5)
                else:
                    print("❌ Número fuera de rango.")
                    time.sleep(1)

        elif sub_opcion == "5":  # AUTO-IMPORTAR
            limpiar_pantalla()
            print("--- 🔍 ESCÁNER DE DIRECTORIOS PROFUNDO ---")
            print(
                "Ingresa la ruta de la carpeta (escaneará subcarpetas automáticamente)."
            )
            print("(Ejemplo: assets o C:/Musica/)")

            ruta_input = input("\n📂 Ruta de la carpeta (o 'X' para cancelar): ")

            if ruta_input.upper() != "X":
                print("\nEscaneando... (Esto puede tomar unos segundos)")
                time.sleep(0.5)

                # AHORA RECIBIMOS DOS VARIABLES:
                cant_canciones, cant_albumes = escanear_carpeta(ruta_input)

                if cant_canciones > 0:
                    print(
                        f"\n✅ ¡Éxito! Se importaron {cant_canciones} pistas y se generaron {cant_albumes} álbumes."
                    )
                else:
                    print("\n⚠️ No se encontraron archivos MP3.")
                time.sleep(2.5)

        elif sub_opcion == "6":
            break
        else:
            print("❌ Opción no válida.")
            time.sleep(1)


def gestionar_playlist(playlist_actual):
    # --- SUB-MENÚ DE LA PLAYLIST SELECCIONADA ---
    while True:
        limpiar_pantalla()
        print(f"\n--- 🎧 PLAYLIST: {playlist_actual.titulo.upper()} ---")
        print(f"Descripción: {playlist_actual.descripcion}")
        print(f"Pistas actuales: {len(playlist_actual.canciones)}")
        print("-----------------------------------")
        print("1. ▶️ Reproducir Playlist")
        print("2. ➕ Agregar Canción (Desde el Catálogo)")
        print("3. ➖ Quitar Canción")
        print("4. 🔙 Volver a Mis Playlists")

        acc = input("\n>> Acción: ")

        if acc == "1":
            if len(playlist_actual.canciones) > 0:
                reproductor.cargar_origen(playlist_actual)
                menu_reproduccion()
            else:
                print("❌ La playlist está vacía. Agrega canciones primero.")
                time.sleep(1.5)

        elif acc == "2":
            # AGREGAR CANCIÓN
            limpiar_pantalla()
            print("--- 🌎 CANCIONES DISPONIBLES ---")
            # Filtramos para mostrar solo Canciones (no Álbumes enteros)
            solo_canciones = [c for c in catalogo_musica if isinstance(c, Cancion)]

            if not solo_canciones:
                print("El catálogo no tiene canciones individuales.")
                input("Presiona Enter...")
                continue

            for i, c in enumerate(solo_canciones):
                print(f"{i+1}. {c.titulo} - {c.artista}")

            try:
                sel = (
                    int(input("\nNúmero de canción a agregar (0 para cancelar): ")) - 1
                )
                if 0 <= sel < len(solo_canciones):
                    cancion_elegida = solo_canciones[sel]
                    # Evitar duplicados exactos en la misma playlist
                    if cancion_elegida in playlist_actual.canciones:
                        print("⚠️ Esta canción ya está en la playlist.")
                    else:
                        playlist_actual.agregar_cancion(cancion_elegida)
                    time.sleep(1.5)
            except ValueError:
                print("❌ Entrada inválida.")
                time.sleep(1)

        elif acc == "3":
            # QUITAR CANCIÓN
            limpiar_pantalla()
            print("--- ➖ QUITAR CANCIÓN ---")
            if not playlist_actual.canciones:
                print("La playlist ya está vacía.")
                time.sleep(1.5)
                continue

            for i, c in enumerate(playlist_actual.canciones):
                print(f"{i+1}. {c.titulo} - {c.artista}")

            try:
                sel = (
                    int(input("\nNúmero de canción a eliminar (0 para cancelar): ")) - 1
                )
                if 0 <= sel < len(playlist_actual.canciones):
                    cancion_quitar = playlist_actual.canciones[sel]
                    playlist_actual.eliminar_cancion(cancion_quitar)
                    time.sleep(1.5)
            except ValueError:
                print("❌ Entrada inválida.")
                time.sleep(1)

        elif acc == "4":
            break  # Sale al menú de "Mis Playlists"
        else:
            print("❌ Opción no válida.")
            time.sleep(1)


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
                    for i, item in enumerate(catalogo_musica):
                        if isinstance(item, Album):
                            print(
                                f"{i+1}. 💿 [ÁLBUM] {item.titulo} - {item.artista} ({len(item._Album__canciones)} pistas)"  # type: ignore
                            )
                        else:
                            print(f"{i+1}. 🎵 [PISTA] {item.titulo} - {item.artista}")

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
                        break  # Sale al menú principal
                    # else:
                    #     for i, pl in enumerate(usuario.mis_playlists):
                    #         print(f"{i+1}. {pl.titulo} ({len(pl.canciones)} canciones)")

                    #     entrada = input(
                    #         "\nElige playlist para reproducir (0 para salir): "
                    #     )
                    #     if entrada.isdigit():
                    #         idx = int(entrada) - 1
                    #         if 0 <= idx < len(usuario.mis_playlists):
                    #             reproductor.cargar_origen(usuario.mis_playlists[idx])
                    #             menu_reproduccion()
                    # Mostrar las listas que tiene el cliente
                    for i, pl in enumerate(usuario.mis_playlists):
                        print(
                            f"{i+1}. {pl.titulo} ({len(pl.canciones)} pistas) - {pl.duracion:.1f} seg"
                        )
                    print("------------------------")

                    entrada = input(
                        "\nElige una playlist para gestionar (0 para salir): "
                    )

                    if entrada == "0":
                        break

                    if entrada.isdigit():
                        idx = int(entrada) - 1
                        if 0 <= idx < len(usuario.mis_playlists):
                            playlist_actual = usuario.mis_playlists[idx]

                            gestionar_playlist(playlist_actual)

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
                else:
                    print("❌ Número de playlist no válido.")
                    time.sleep(1)

            elif isinstance(usuario, Administrador):
                if opcion == "1":
                    gestionar_catalogo()

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
            print("\n\nApagando Notify... ¡Adiós!")
            break
