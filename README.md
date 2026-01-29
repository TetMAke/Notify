# Spotipy - Consola de Reproducción Musical en Python

**Spotipy** es una simulación de plataforma de streaming de música desarrollada en Python. Este proyecto fue diseñado con un enfoque educativo para demostrar la implementación robusta de los **4 Pilares de la Programación Orientada a Objetos (POO)** y arquitectura de software modular.

El sistema permite la gestión de usuarios con roles jerárquicos (Clientes y Administradores), creación de playlists y reproducción de audio real utilizando la librería `pygame-ce`.

## 📋 Características Principales

- **Sistema de Roles Jerárquico:**
  - **Clientes:** Pueden explorar el catálogo, reproducir música, crear playlists personales y gestionar sus "Me Gusta".
  - **Administradores:** Heredan todas las capacidades del cliente ("God Mode") y añaden herramientas de gestión (monitor de usuarios, bloqueo, gestión de catálogo global).
- **Reproductor Híbrido:**
  - Soporte para reproducción de audio real (MP3) mediante `pygame-ce`.
  - Simulación en consola para metadatos y control de flujo.
- **Gestión de Datos:** Estructuras de datos eficientes para el manejo de librerías musicales y perfiles de usuario.

## 🛠️ Tecnologías y Conceptos Aplicados

### Lenguaje y Librerías
* **Python 3.x**
* **pygame-ce** (Community Edition) para el motor de audio.

### Arquitectura de Software
El proyecto sigue una arquitectura modular separando responsabilidades:
* `modelos/`: Definición de Entidades (Usuario, Cancion, Playlist).
* `servicios/`: Lógica de negocio y controladores (Reproductor, Autenticación).
* `utils/`: Manejo de excepciones personalizadas y helpers.

### Pilares de la POO Implementados
1.  **Abstracción:** Modelado de clases complejas (`Usuario`, `RecursoMultimedia`) simplificando la complejidad interna del streaming.
2.  **Encapsulamiento:** Protección de datos sensibles (contraseñas, atributos internos de gestión) y uso de *getters/setters* pythonicos (`@property`).
3.  **Herencia:** Jerarquía lineal optimizada (`Usuario` -> `Cliente` -> `Administrador`) para reutilización de código (DRY).
4.  **Polimorfismo:** Métodos compartidos con comportamientos distintos según el contexto (ej: `reproducir()` funciona diferente en una `Cancion` individual que en una `Playlist`).

## 📂 Estructura del Proyecto

```text
Spotipy/
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── assets/
│   └── musica/               # Archivos .mp3 locales
├── modelos/
│   ├── usuario.py            # Clases: Usuario, Cliente, Administrador
│   └── multimedia.py         # Clases: Cancion, Album, Playlist
├── servicios/
│   ├── reproductor.py        # Wrapper para pygame.mixer
│   └── autenticacion.py      # Lógica de login y registro
└── utils/
    └── excepciones.py        # Errores personalizados (AuthError, etc.)
```

## 🚀 Instalación y Uso

1.  **Clonar o descargar el repositorio.**
2.  **Instalar dependencias:**
    Abre tu terminal en la carpeta del proyecto y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Agregar música:**
    Coloca tus archivos `.mp3` dentro de la carpeta `assets/musica/`.
    *(El sistema detectará automáticamente los archivos en esta carpeta)*.
4.  **Ejecutar:**
    ```bash
    python main.py
    ```

## 👤 Autor

**Silfri Medina**
*Docente de Matemáticas & Desarrollador Python*

Este proyecto fue construido desde cero para consolidar conocimientos en Ingeniería de Software, aplicando principios SOLID y los 4 pilares de la POO.

📫 **Contacto:**
* **LinkedIn:** [Pegar enlace a tu perfil aquí]
* **Email:** [Tu correo electrónico]
* **GitHub:** [Enlace a tu perfil de GitHub]