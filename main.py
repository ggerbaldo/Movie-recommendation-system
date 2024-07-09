# Este código define una API web simple para recomendar películas usando FastAPI. A continuación se detalla su funcionamiento:

# Importación de librerías:
from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carga de los DataFrames:
df_movies = pd.read_parquet('Data/df_movies.parquet')
df_recommend = pd.read_csv('Data/df_recommend.csv')

# Creación del vectorizador:
vectorizer = TfidfVectorizer()
# Creación de la matriz TF-IDF:
matrix = vectorizer.fit_transform(df_recommend['title'] + ' ' + df_recommend['genres'].astype(str) + ' ' + df_recommend['actors'].astype(str) + ' ' + df_recommend['production_companies'].astype(str) + ' ' + df_recommend['directors'].astype(str) + ' ' + df_recommend['genres'].astype(str) + ' ' + df_recommend['genres'].astype(str))

# Restablecimiento del índice de df_recommend:
df_recommend = df_recommend.reset_index(drop=True)

# Calculamos la matriz de similitud de coseno (cuanto más alto el valor, mayor similitud).
cosine_matrix = cosine_similarity(matrix)

# Se crea una instancia de la clase FastAPI
app = FastAPI()

# Definición del endpoint, a través del decorador:
@app.get("/")

# Función con mensaje de bienvenida
def index():
    return {"¡Bienvenidos al Proyecto Individual nro 1 de Guillermo Gerbaldo!"}

# Definición del endpoint y función de cantidad de filmaciones por mes.
@app.get("/meses/{Mes}")

def cantidad_filmaciones_mes(Mes:str):
    
    # Se define un diccionario que asocia cada mes en español con un número
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'setiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    # Se obtiene el número de mes correspondiente al nombre del mes ingresado convirtiendolo a minúsculas y buscandolo en el diccionario anterior.
    mes_numero = meses.get(Mes.lower(), None)
    # Si no se encuentra el mes en el diccionario, se devuelve un mensaje de error indicando que el mes no es válido.
    if mes_numero is None:
        return f"No se reconoce el mes '{Mes}'. Por favor, ingresa un mes válido en español."
    # Se selecciona un subconjunto del DataFrame df_movies que contiene solo las películas cuya fecha de estreno (release_date) corresponde al mes especificado.
    peliculas_mes = df_movies[df_movies['release_date'].dt.month == mes_numero]
    # Se cuenta la cantidad de películas en el subconjunto seleccionado.
    cantidad = len(peliculas_mes)
    # Se devuelve un mensaje que indica la cantidad de películas estrenadas en el mes, utilizando la forma singular o plural de "película" según la cantidad.
    return f"{cantidad} {'películas' if cantidad != 1 else 'película'} fueron estrenadas en el mes de {Mes.capitalize()}."

# Definición del decorador para endpoint y función de cantidad de filmaciones por día.
@app.get("/dias/{Dia}")

def cantidad_filmaciones_dia(Dia:str):
    # Convierte a columna a formato datetime, necesario para poder acceder a atributos relacionados como el día de la semana.
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    # Se define un diccionario dias que asocia cada día de la semana en español a su número correspondiente (de 0 a 6).
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5,'domingo': 6}
    # Se obtiene el número de día correspondiente al nombre del día ingresado (Dia) convirtiendolo a minúsculas y buscándolo en el diccionario.
    dia_numero = dias.get(Dia.lower(), None)
    # Si no se encuentra el día en el diccionario, se devuelve un mensaje de error indicando que el día no es válido.
    if dia_numero is None:
        return f"No se reconoce el día '{Dia}'. Por favor, ingresa un día válido en español."
    # Se selecciona un subconjunto del DataFrame df_movies que contiene solo las películas cuya fecha de estreno (release_date) corresponde al día de la semana especificado.
    peliculas_dia = df_movies[df_movies['release_date'].dt.dayofweek == dia_numero]
    # Se cuenta la cantidad de películas en el subconjunto seleccionado y se imprime resultado.
    cantidad = len(peliculas_dia)
    return f"{cantidad} {'películas' if cantidad != 1 else 'película'} fueron estrenadas en los días {Dia.title()}."

# Se define decorador para un endpoint en una API web que permite obtener información sobre una película específica, incluyendo su año de estreno y su score/popularidad, a partir de su título.
@app.get("/score/{Score}")

def score_titulo(titulo_de_la_filmacion:str):
    # Conversión de la fecha de estreno a formato datetime para poder trabajar con los atributos relacionados.
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    # Se convierte el título de la película ingresado por el usuario (titulo_de_la_filmacion) a minúsculas utilizando el método lower() para realizar una búsqueda no sensible a mayúsculas y minúsculas.
    titulo_ingresado_lower = titulo_de_la_filmacion.lower()
    # Se selecciona una subfila del DataFrame df_movies que contiene solo la información de la película con el título coincidente (en minúsculas).
    pelicula = df_movies[df_movies['title'].str.lower() == titulo_ingresado_lower]
    # Si está vacía, se devuelve un mensaje de error indicando que no se encontró información para la película.
    if pelicula.empty:
        return f"No se encontró información para la película '{titulo_de_la_filmacion}'."
    else:
        # Si la película se encuentra, se extraen los siguientes datos de la subfila y se imprime resultado:
        titulo_original = pelicula['title'].iloc[0]
        año_estreno = pelicula['release_date'].dt.year.iloc[0]
        score = pelicula['popularity'].iloc[0]
        return f"La película '{titulo_original}' fue estrenada en el año {año_estreno} con un score/popularidad de {score:.2f}."

# Definimos decorador para un endpoint que permite obtener información sobre una película específica, incluyendo su año de estreno, su cantidad de valoraciones y su valoración promedio, a partir de su título.   
@app.get("/votes/{Votos}")

def votos_titulo(titulo_de_la_filmacion):
    # Conversión de la fecha de estreno a formato datetime:
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    # Se convierte el título de la película ingresado por el usuario (titulo_de_la_filmacion) a minúsculas utilizando el método lower().
    titulo_ingresado_lower = titulo_de_la_filmacion.lower()
    # Se selecciona una subfila del DataFrame df_movies que contiene solo la información de la película con el título coincidente (en minúsculas).
    pelicula = df_movies[df_movies['title'].str.lower() == titulo_ingresado_lower]
    # Si no se encuentra ninguna película con el título ingresado se devuelve un mensaje de error indicando que no se encontró información para la película.
    if pelicula.empty:
        return f"No se encontró información para la película '{titulo_de_la_filmacion}'."
    else:
        # Si la pelicula se encuentra se verifican los votos, titulo original, promedio de popularidad, siempre que la cantidad de votos sea mayor a 2000.
        votos = int(pelicula['vote_count'].iloc[0])
        if votos < 2000:
            return f"La película '{titulo_de_la_filmacion}' fue estrenada en el año {pelicula['release_date'].dt.year.iloc[0]}. La misma cuenta con menos de 2000 valoraciones."
        else:
            titulo_original = pelicula['title'].iloc[0]
            promedio = round(pelicula['popularity'].iloc[0], 2)
            return f"La película '{titulo_original}' fue estrenada en el año {pelicula['release_date'].dt.year.iloc[0]}. Tiene un total de {votos} valoraciones, con un promedio de {promedio}."


#  Decorador para un endpoint en una API web que permite obtener información sobre un actor específico, incluyendo la cantidad de películas en las que ha participado y su retorno promedio, y que a su vez, NO HAYA SIDO EL DIRECTOR DE LA MISMA.
@app.get("/actor/{Actor}")

def get_actor(nombre_actor:str):
    # Se convierte el nombre del actor ingresado por el usuario (nombre_actor) a minúsculas utilizando el método lower(), para obviar si es mayuscula o minuscula.
    nombre_actor_lower = nombre_actor.lower()
    # Se selecciona un subconjunto del DataFrame df_movies que contiene solo las películas donde el nombre del actor (en minúsculas) se encuentra en la columna actors Y NO en la columna director.
    peliculas_actor = df_movies[df_movies['actors'].str.lower().str.contains(nombre_actor_lower, na=False) &
        (~df_movies['director'].str.lower().str.contains(nombre_actor_lower, na=False))]
    # Verifica si el subconjunto seleccionado está vacío, y devuelve un mensaje de error indicando que no se encontró información para el actor.
    if peliculas_actor.empty:
        return f"No se encontró información para el actor '{nombre_actor}'."
    else:
        # Si es positiva la búsqueda, suma las peliculas encontradas, calcula su retorno promedio e imprime resultado. 
        cantidad_peliculas = len(peliculas_actor)
        retorno_promedio = peliculas_actor['return'].mean()
        return f"{nombre_actor} ha participado en {cantidad_peliculas} {'filmaciones' if cantidad_peliculas != 1 else 'filmación'}, con un retorno promedio de ${retorno_promedio:.2f}."


# Este decorador define un endpoint para una API web que permite obtener información sobre un director específico, incluyendo la cantidad de películas que ha dirigido, su retorno total y detalles de cada película dirigida. 
@app.get("/director/{Director}")

def get_director(nombre_director:str):
    #  Se convierte la columna release_date del DataFrame df_movies a formato datetime.
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    # Se convierte el nombre del director ingresado por el usuario (nombre_director) a minúsculas utilizando el método lower() para evitar sensibilidad entre mayusculas/minusculas.
    nombre_director_lower = nombre_director.lower()
    # Se selecciona solo las películas donde el nombre del director (en minúsculas) se encuentra en la columna director.
    peliculas_director = df_movies[df_movies['director'].str.lower().str.contains(nombre_director_lower, na=False)]
    # Verifica si está vacío, significa que no se encontró información para el director ingresado.En este caso, se devuelve un mensaje de error indicando que no se encontró información para el director.
    if peliculas_director.empty:
        return f"No se encontró información para el director '{nombre_director}'."
    else:
        # Se calcula la cantidd de peliculas de acuerdo a la extención de objetos.
        cantidad_peliculas = len(peliculas_director)
        # Se calcula el retorno total sumando el retorno individual de las peliculas del director.
        retorno_total = round(peliculas_director['return'].sum(), 2)
        # Se crea una lista vacia donde se cargaran los detalles siguientes en el recorrido del dataframe a traves de un bucle for: Nnombre pelicula, fecha de lanzamiento, retorno individual, costo, ganancia.
        detalles_peliculas = []
        for _, row in peliculas_director.iterrows():
            nombre_pelicula = row['title']
            fecha_lanzamiento = row['release_date'] #.strftime("%Y-%m-%d")
            retorno_individual = row['return']
            costo = row['budget']
            ganancia = row['revenue']
            detalles_peliculas.append(f"{nombre_pelicula} (Lanzamiento: {fecha_lanzamiento}, Retorno: {retorno_individual:2f}, Costo: {costo}, Ganancia: {ganancia})")
        peliculas_formateadas = "\n".join(detalles_peliculas)
        return f"El director '{nombre_director}' ha dirigido {cantidad_peliculas} {'películas' if cantidad_peliculas != 1 else 'película'}, con un retorno total de {retorno_total}.\nDetalles de las películas:\n{peliculas_formateadas}"
    
# Este decorador define un endpoint para una API web que permite obtener recomendaciones de 5 películas similares a una película específica.
@app.get("/recommend/{Recomendarpelículas}", response_model=List[str])  # Se define el tipo de dato de retorno.

def recomendacion(titulo: str):
    # Se define una función llamada recomendacion que recibe un parámetro de entrada titulo de tipo cadena de texto y se convierte todo a lower para trabajar en minusculas.
    titulo = titulo.lower()
    titulo_pelicula = df_recommend[df_recommend['title'].str.lower() == titulo]

    # Se verifica si la subfila seleccionada está vacía. En este caso, se genera una excepción HTTPException con código de estado 404 (No encontrado) y un mensaje de error indicando que no se encontró la película.
    if titulo_pelicula.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró la película {titulo}")

    # Si la película se encuentra, se obtiene su índice dentro del DataFrame utilizando el atributo index[0]. el cual se utiliza para acceder a la fila correspondiente de la matriz de similitudes coseno.
    indice_producto = titulo_pelicula.index[0]
    # Se calcula el vector de similitudes coseno para la película utilizando la matriz cosine_matrix y el índice obtenido en el paso anterior.
    similitudes_producto = cosine_matrix[indice_producto]
    # Se ordenan las similitudes en orden descendente y se seleccionan los 5 índices con mayor similitud excluyendo el índice de la película original. Se imprime lista.
    indices_top_5_similares = np.argsort(-similitudes_producto)[1:6]
    top_5_peliculas = df_recommend.loc[indices_top_5_similares, 'title'].tolist()  # Convierte a lista
    return top_5_peliculas

