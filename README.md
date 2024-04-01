# Formula 1 Web App

¡Bienvenido a la página Formula 1 Web App! Aquí encontrarás una plataforma completa para explorar y analizar los datos de la Fórmula 1 desde 1960 hasta la actualidad. A continuación, te proporcionamos una guía sobre las principales funcionalidades de esta página.

## Descarga de Datos de Resultados

- Descarga los datos completos de los resultados de cada temporada de Fórmula 1 desde 1960 hasta la actualidad.
- Utiliza la sección de "Actualizar Base de Datos" de la parte superior derecha para obtener archivos en formatos compatibles con análisis de datos.

## Consulta de Clasificación

- Accede a la sección "Clasificación" para consultar la clasificación actualizada hasta cualquier jornada de la temporada descargada.

## Información de Pilotos

- Consulta la información detallada de cualquier piloto en una temporada específica.
- Disfruta de gráficos interactivos que muestran el histórico de posiciones del piloto a lo largo de la temporada.

## Creación y Comparación de Grafos Competitivos

- Crea y compara grafos competitivos ponderados y no ponderados hasta cualquier jornada de la temporada descargada.
- Analiza el cambio de posiciones entre los pilotos y los grupos de competitivad que se crean a lo largo de una temporada

## Cálculo de Métricas de Competitividad

- Descubre las métricas de competitividad para una jornada en concreto de una temporada descargada.
- Obtén insights sobre la competitividad de cada temporada.

## Gráficas Interactivas de Métricas de Competitividad

- Explora gráficas interactivas que destacan las métricas de competitividad de una jornada específica.
- Compara la competitividad entre los diferentes pilotos

# Requisitos Técnicos

- Python 3.7 o superior.

# Guía de Configuración

## Entorno local

Sigue estos pasos para configurar y ejecutar la aplicación en tu entorno local:

1. Clona el repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone https://github.com/AlejandroAdrados/F1-webapp
```

2. Navega al directorio del proyecto recién clonado con el siguiente comando:

```bash
cd F1-webapp
```

3. Crea un entorno virtual para este proyecto y actívalo. Esto te ayudará a mantener las dependencias del proyecto aisladas de otros proyectos y del sistema global de Python. Usa los siguientes comandos:

```bash
python3 -m venv venv         # Crear un entorno virtual llamado 'venv'
source venv/bin/activate     # Activar el entorno virtual en macOS/Linux
.\venv\Scripts\activate      # Activar el entorno virtual en Windows (PowerShell)
```

4. Instala las dependencias del proyecto utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```

5. Ahora puedes ejecutar la aplicación con el siguiente comando:

```bash
python3 run.py
```

6. Abre tu navegador web y accede a la página utilizando la siguiente URL:

```
http://localhost:8050
```

## Entorno dockerizado

Sigue estos pasos para configurar y ejecutar la aplicación en un contenedor docker:

1. Clona el repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone https://github.com/AlejandroAdrados/F1-webapp
```

2. Navega al directorio del proyecto recién clonado con el siguiente comando:

```bash
cd F1-webapp
```

3. Construye la imagen:

```bash
docker build -t f1-webapp .
```

4. Ejecuta la imagen construida:

```bash
docker run -p 8050:8050 --name F1-webapp f1-webapp
```

5. Abre tu navegador web y accede a la página utilizando la siguiente URL:

```
http://localhost:8050
```
##

¡Disfruta explorando los fascinantes datos de la Fórmula 1!
