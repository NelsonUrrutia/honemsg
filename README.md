![Honemsg](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/honemsg-logo.svg)

![Honemsg en uso: pantalla de inicio, traducción de un PR y mejora de documentación técnica](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/honemsg-cover.png)

---

> **Honemsg** es una  TUI - *Terminal User Interface* -  que "afila" la redacción de tus mensajes con un modelo de IA local.

He desarrollado **Honemsg** con el objetivo de mejorar la redacción de mis mensajes, tanto internos como con clientes, en inglés y español. 

Mi idea fue crear una herramienta que me ayude a mejorar la redacción de mis mensajes, corrija
errores gramaticales, elimine redundancias y haga más claro lo que quiero transmitir.

Inicialmente, utilizaba ChatGPT para esta tarea, pero vi una oportunidad para crear una herramienta propia. Decidí utilizar Ollama y sus modelos locales, lo que me permite mejorar los mensajes sin incurrir en costes. 

Y la clave fue identificar mi necesidad: "necesito un asistente que me ayude a mejorar el mensaje que quiero enviar, no me hace falta que tenga todo el contexto; eso ya lo tengo en mi mente". Y así fue como surgió la idea de **Honemsg**; en inglés *hone* significa afilar.

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

Instálalo con `pipx` desde [PyPI](https://pypi.org/project/honemsg/):

```bash
pipx install honemsg
```

> `pipx` crea un entorno virtual propio para la aplicación y deja el comando `honemsg` disponible en tu terminal, sin interferir con otros paquetes de Python.

### 3. Ejecuta la aplicación

Asegúrate de que Ollama está en ejecución (la app de escritorio o `ollama serve`) y lanza:

```bash
honemsg
```

Se abrirá la TUI desde la que puedes empezar a mejorar tus mensajes.

Para salir de la aplicación, pulsa <kbd>Ctrl</kbd> + <kbd>Q</kbd>.

### Actualizar y desinstalar

```bash
pipx upgrade honemsg     # actualizar a la última versión
pipx uninstall honemsg   # desinstalar
```

## Honemsg en acción

### Mensaje de Slack en inglés

![Honemsg mejorando un mensaje de Slack en inglés](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/test-one.gif)

### Mensaje de Slack en español

![Honemsg mejorando un mensaje de Slack en español](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/test-two.gif)

### Documentación: guía técnica

![Honemsg mejorando documentación técnica en Markdown](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/doc-improvement.gif)

### Documentación: informe de investigación

![Honemsg mejorando un informe de investigación en Markdown](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/test-doc-improve.gif)

### Email

![Honemsg mejorando un email](https://raw.githubusercontent.com/NelsonUrrutia/honemsg/main/assets/test-four.gif)
