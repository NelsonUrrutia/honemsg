```text
╒════╗╒════╗ ╒═════════╗  ╒════╗   ╒════╗ ╒═════════╗  ╒════════════╗  ╒═════════╗ ╒════════╗
└┐  ╓╜└┐  ╓╜ │  ╓───┐  ║  │    ╚╗  └┐  ╓╜ └┐  ╓───┐ ║  │  ╓─┐  ╓─┐  ║  │  ╓────┐ ║ │  ╓───┐ ║
 │  ║  │  ║  │  ║   │  ║  │  ╟┐ ╚╗  │  ║   │  ║   └─╜  │  ║ │  ║ │  ║  │  ║    └─╜ │  ║   └─╜
 │  ╚══╛  ║  │  ║   │  ║  │  ║└┐ ╚╗ │  ║   │  ╚══╗     │  ║ │  ║ │  ║  │  ╚══════╗ │  ║
 │  ╓──┐  ║  │  ║   │  ║  │  ║ └┐ ╚╗│  ║   │  ╓──╜     │  ║ │  ║ │  ║  └──────┐  ║ │  ║ ╒════╗
 │  ║  │  ║  │  ║   │  ║  │  ║  └┐ ╚╡  ║   │  ║   ╒═╗  │  ║ └──╜ │  ║  ╒═╗    │  ║ │  ║ └┐  ╓╜
╒╛  ╚╗╒╛  ╚╗ │  ╚═══╛  ║ ╒╛  ╚╗  └┐    ║  ╒╛  ╚═══╛ ║ ╒╛  ╚╗    ╒╛  ╚╗ │ ╚════╛  ║ │  ╚══╛  ║
└────╜└────╜ └─────────╜ └────╜   └────╜  └─────────╜ └────╜    └────╜ └─────────╜ └────────╜
```

# Honemsg

---

> **Honemsg** es una  TUI - *Terminal User Interface* -  que "afila" la redacción de tus mensajes con un modelo de IA local.

He desarrollado **Honemsg** con el objetivo de mejorar la redacción de mis mensajes, tanto internos como con clientes, en inglés y español. 

Mi idea fue crear una herramienta que me ayude a mejorar la redacción de mis mensajes, corrija
errores gramaticales, elimine redundancias y haga más claro lo que quiero transmitir.

Inicialmente, utilizaba ChatGPT para esta tarea, pero vi una oportunidad para crear una herramienta propia. Decidí utilizar Ollama y sus modelos locales, lo que me permite mejorar los mensajes sin incurrir en costes. 

Y la clave fue identificar mi necesidad: "necesito un asistente que me ayude a mejorar el mensaje que quiero enviar, no me hace falta que tenga todo el contexto; eso ya lo tengo en mi mente". Y así fue como surgió la idea de **Honemsg**.

## Stack

1. Python - Lógica e interfaz gráfica - usando [Textual](https://textual.textualize.io/).
2. [Ollama](https://ollama.com/) y [translategemma](https://ollama.com/library/translategemma)

## Instalación

### Requisitos

- [Python](https://www.python.org/downloads/) 3.10 o superior.
- [pipx](https://pipx.pypa.io/stable/installation/) para instalar la aplicación de forma aislada.
- [Ollama](https://ollama.com/download) con el modelo `translategemma` descargado.

### 1. Instala Ollama y el modelo

1. Descarga e instala [Ollama](https://ollama.com/download) siguiendo los pasos para tu sistema operativo.
2. Descarga el modelo [translategemma](https://ollama.com/library/translategemma):

   ```bash
   ollama pull translategemma
   ```

3. Comprueba que el modelo aparece en la lista:

   ```bash
   ollama list
   ```

> [!NOTE]
> Por ahora **Honemsg** usa el modelo `translategemma:latest` de forma fija. Si descargas otro modelo, la aplicación no lo utilizará.

### 2. Instala Honemsg

Instálalo con `pipx` directamente desde el repositorio:

```bash
pipx pipx install
```

> `pipx` crea un entorno virtual propio para la aplicación y deja el comando `honemsg` disponible en tu terminal, sin interferir con otros paquetes de Python.

### 3. Ejecuta la aplicación

Asegúrate de que Ollama está en ejecución (la app de escritorio o `ollama serve`) y lanza:

```bash
honemsg
```

Se abrirá la TUI desde la que puedes empezar a mejorar tus mensajes.

### Actualizar y desinstalar

```bash
pipx upgrade honemsg     # actualizar a la última versión
pipx uninstall honemsg   # desinstalar
```

### Instalación para desarrollo

Si quieres modificar el código, clona el repositorio e instálalo en modo editable:

```bash
git clone https://github.com/NelsonUrrutia/honemsg.git
cd honemsg
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -e .
honemsg
```

## Honemsg en acción
