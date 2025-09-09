Simulación y Modelación: Generador y Pruebas de Números Pseudoaleatorios
Este proyecto es una aplicación de escritorio desarrollada en Python con CustomTkinter para la interfaz gráfica. Su propósito es generar secuencias de números pseudoaleatorios usando diferentes algoritmos y someterlos a pruebas estadísticas para validar su calidad. La herramienta permite visualizar tanto los resultados numéricos como los gráficos.

💻 Requisitos y Pasos de Ejecución
Para ejecutar esta aplicación, necesitarás tener Python 3.10 o una versión superior instalada. Las siguientes librerías de Python son obligatorias:

1. Instala las librerías:
Abre una terminal o línea de comandos y ejecuta los siguientes comandos:
pip install customtkinter
pip install matplotlib
pip install scipy
pip install numpy

2. Ejecuta la aplicación:
Una vez que las librerías estén instaladas, navega hasta la carpeta del proyecto y ejecuta el archivo principal:
python main.py

Capturas de Pantalla de la GUI
A continuación, se muestran las interfaces principales del programa.

Menú de Generadores de Números:
(Aquí deberías pegar una imagen de tu menú principal, donde se pueden seleccionar los algoritmos como Cuadrados Medios, etc.)

Resultados de un Algoritmo de Generación:
(Aquí deberías pegar una imagen de la pantalla que muestra la tabla de resultados de un algoritmo, con los botones de prueba y exportar).

Prueba de Varianza:
(Aquí deberías pegar una imagen de la interfaz de la Prueba de Varianza, mostrando los campos de entrada y los resultados).

Gráfico de Histograma:
(Aquí deberías pegar una imagen del histograma que se genera en la Prueba de Uniformidad).

Bitácora de Avances por Clase
Clase 1: Se creó la estructura básica del proyecto con la interfaz principal. Se implementó el Algoritmo de Cuadrados Medios para la generación de números pseudoaleatorios.

Clase 2: Se añadieron los Algoritmos de Productos Medios y Multiplicador Constante. Se implementó la Prueba de Medias para validar la calidad de la media.

Clase 3: Se incorporaron las pruebas de calidad restantes: Prueba de Varianza y Prueba de Uniformidad (Chi-cuadrada). Se añadieron los gráficos correspondientes a cada prueba para una mejor visualización.

Clase 4: Se refactorizó el código para separar la lógica de negocio (logica.py) de la interfaz de usuario (main.py). Se añadió un botón para Exportar resultados a un archivo de texto (.txt) en cada una de las pantallas de resultados.