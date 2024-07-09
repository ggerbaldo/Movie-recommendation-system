![image](https://github.com/ggerbaldo/Proyecto1/assets/101016328/042707d0-b119-4478-a93a-a2fcd28d5e5a)

### Proyecto individual nº1 - Guillermo Gerbaldo
======================================
# _*Machine Learning Operations (MLOps)*_


![image](https://github.com/ggerbaldo/Proyecto1/assets/101016328/a4617d9f-2f15-4c0c-b9c0-f8b17d4bd626)






-----------------------------------------
## Descripción y objeto del proyecto
Este proyecto tiene como objetivo aplicar los conocimientos adquiridos durante los seis módulos de la carrera de Data Science en Soy Henry. A través del framework FastAPI, pondremos a disposición la información transformada de una base de datos relacionada con el mundo cinematográfico. Entre las funcionalidades disponibles se encuentra un Sistema de Recomendación de Películas, así como consultas sobre información de películas, directores, actores y la recepción del público. Utilizaremos técnicas de Machine Learning para analizar el historial de valoración, puntuaciones y patrones de comportamiento de los usuarios. Además, desplegaremos una API de acceso público que permitirá explorar diversos aspectos del mundo del cine.. (link: https://proyecto1-cp3v.onrender.com). 



## Aspectos iniciales:
Hemos recibido una base de datos en dos archivos en formato CSV (Comma Separated Values) con aproximadamente 45,000 registros. Nuestra tarea consiste en procesar y transformar estos datos (ETL) utilizando la herramienta Visual Studio Code, para crear seis funciones que se consumirán a través de una API. Además, implementaremos un modelo de recomendación de películas y presentaremos los resultados para uso público en un entorno de Render. Para lograrlo, realizaremos un Análisis Exploratorio de los Datos (EDA) con el objetivo de mejorar la implementación del modelo.

## Extracción, Carga y Transformación de los datos (ETL).

Analizamos y transformamos el archivo **credits.csv**:
En este archivo, encontramos tres campos:
ID de la película
CAST: Información detallada sobre los actores, incluyendo su ID particular, nombre del personaje representado y género.
CREW: Información sobre los distintos roles en el desarrollo de una película, como directores, productores, guionistas, editores y directores de fotografía.
Hemos identificado la necesidad de desanidar las distintas columnas para obtener únicamente los actores y directores. Como primer paso, hemos separado ambos campos en dos dataframes y los hemos desanidado para quedarnos con el ID de la película y el nombre del actor y director. Este proceso nos permite reducir el tamaño de los conjuntos de datos al eliminar información que no utilizaremos.

Analizamos y transformamos el archivo **movies_dataset.csv**:

Este archivo proporciona detalles sobre las películas, incluyendo:
Título
Colección a la que pertenece
Presupuesto
Idioma
Género
Breve reseña
Popularidad
Cantidad de votos
Compañía productora
País de producción
Ganancias
Fecha de lanzamiento
Estado (lanzada o en producción)

Como primera medida, se eliminan un conjunto de columnas solicitadas se verifica y eliminan nulos, se convierten registros de texto a números. También se crea el campo RETORNO solicitado, dividiendo la GANANCIA por el PRESUPUESTO y se suprimen espacios en blanco en el campo TITULO. Finalmente, se unen los distintos dataframe, para el desarrollo de las funciones solicitadas.


## Creación de las funciones.

- **cantidad_filmaciones_mes**: Esta función devuelve la cantidad de películas lanzadas en un mes específico. Al seleccionar un mes, obtendremos el número total de filmaciones, independientemente del año. Como particularidad, hemos creado un diccionario con los nombres de los meses en español para facilitar la búsqueda, hemos incluido “SETIEMBRE/SEPTIEMBRE” para que acepte ambos términos. Además, se incluye una sentencia para que el código no distinga entre mayúsculas y minúsculas.

- **cantidad_filmaciones_dia**: Similar a la anterior, esta función devuelve la cantidad de películas lanzadas en un día específico. Al seleccionar un día, obtendremos el número total de filmaciones, independientemente del mes o año. También, hemos creado un diccionario con los nombres de los días en español para facilitar la búsqueda, en este caso se incluyeron las opciones con o sin tilde de SÁBADO/SABADO y MIÉRCOLES/MIERCOLES. Tabién, se incluye una sentencia para que el código no distinga entre mayúsculas y minúsculas.

- **score_titulo**: Esta función nos brinda información sobre una película específica, incluyendo su año de estreno y su score/popularidad, a partir de su título. Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.

- **votos_titulo**: Esta función nos permite obtener información sobre una película específica, incluyendo su año de estreno, su cantidad de valoraciones y su valoración promedio, a partir de su título. 

- **get_actor**: Esta función permite obtener información sobre un actor específico, incluyendo la cantidad de películas en las que ha participado y su retorno promedio, y que a su vez, NO HAYA SIDO EL DIRECTOR DE LA MISMA.

- **get_director**: Esta función brinda información sobre un director específico, incluyendo la cantidad de películas que ha dirigido, su retorno total y detalles de cada película dirigida (título, fecha de lanzamiento, retorno individual, costo, costo y ganancia de la misma.

 
## Análisis Exploratorio de Datos (EDA).

En esta parte del proyecto donde desarrollaremos un modelo para recomendar 5 peliculas de acuerdo a una indicada, utilizaremos una serie de herramientas que nos ayudarán en el análisis y exploración de los datos: **seaborn**, **matplotlib**, **ydata-profiling**.
Partimos del dataset transformado en el proceso de ETL, analizamos los campos utlizando algunos gráficos y nube de palabras y se decide utilizar el modelo de Similitid del Coseno para trabajar con los campos categóricos. Para ello, realizamos una breve transformación en el dataframe, reagrupando las columnas Director y Actores, para que cada registro/fila de pelicula encuentre sus actores y directores en un sólo campo como listas. Posteriormente, se crea la función **recomendacion** y se suma a la FastAPI, para luego deployar todo el código **main.py** en el Render.

---------------------------------------------
