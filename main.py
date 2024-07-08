from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

<<<<<<< HEAD
df_movies = pd.read_parquet('C:\\Users\\felip\\Desktop\\Proyecto1\\Data\\df_movies.parquet')
df_recommend = pd.read_parquet('C:\\Users\\felip\\Desktop\\Proyecto1\\Data\\df_recommend.parquet')
=======
df_movies = pd.read_parquet('Data/df_movies.parquet')
df_recommend = pd.read_parquet('Data/df_recommend.parquet')
>>>>>>> e0af8d68828f6f5576a3021aa56179a16c34b203

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(df_recommend['title'] + ' ' + df_recommend['genres'].astype(str) + ' ' + df_recommend['actors'].astype(str) + ' ' + df_recommend['production_companies'].astype(str) + ' ' + df_recommend['directors'].astype(str) + ' ' + df_recommend['genres'].astype(str) + ' ' + df_recommend['genres'].astype(str))

df_recommend = df_recommend.reset_index(drop=True)

# Calculamos la matriz de similitud de coseno
cosine_matrix = cosine_similarity(matrix)

app = FastAPI()
<<<<<<< HEAD

=======
                          
>>>>>>> e0af8d68828f6f5576a3021aa56179a16c34b203
@app.get("/")

def index():
    return {"¡Bienvenidos al Proyecto Individual nro 1 de Guillermo Gerbaldo!"}

@app.get("/meses/{Mes}")

def cantidad_filmaciones_mes(Mes:str):
    
    meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'setiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    mes_numero = meses.get(Mes.lower(), None)
    if mes_numero is None:
        return f"No se reconoce el mes '{Mes}'. Por favor, ingresa un mes válido en español."
    peliculas_mes = df_movies[df_movies['release_date'].dt.month == mes_numero]
    cantidad = len(peliculas_mes)
    return f"{cantidad} {'películas' if cantidad != 1 else 'película'} fueron estrenadas en el mes de {Mes.capitalize()}."

@app.get("/dias/{Dia}")

def cantidad_filmaciones_dia(Dia:str):
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5,'domingo': 6}
    dia_numero = dias.get(Dia.lower(), None)
    if dia_numero is None:
        return f"No se reconoce el día '{Dia}'. Por favor, ingresa un día válido en español."
    peliculas_dia = df_movies[df_movies['release_date'].dt.dayofweek == dia_numero]
    cantidad = len(peliculas_dia)
    return f"{cantidad} {'películas' if cantidad != 1 else 'película'} fueron estrenadas en los días {Dia.title()}."

@app.get("/score/{Score}")

def score_titulo(titulo_de_la_filmacion:str):
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    titulo_ingresado_lower = titulo_de_la_filmacion.lower()
    pelicula = df_movies[df_movies['title'].str.lower() == titulo_ingresado_lower]
    if pelicula.empty:
        return f"No se encontró información para la película '{titulo_de_la_filmacion}'."
    else:
        titulo_original = pelicula['title'].iloc[0]
        año_estreno = pelicula['release_date'].dt.year.iloc[0]
        score = pelicula['popularity'].iloc[0]
        return f"La película '{titulo_original}' fue estrenada en el año {año_estreno} con un score/popularidad de {score:.2f}."
    
@app.get("/votes/{Votos}")

def votos_titulo(titulo_de_la_filmacion):
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    titulo_ingresado_lower = titulo_de_la_filmacion.lower()
    pelicula = df_movies[df_movies['title'].str.lower() == titulo_ingresado_lower]
    if pelicula.empty:
        return f"No se encontró información para la película '{titulo_de_la_filmacion}'."
    else:
        votos = int(pelicula['vote_count'].iloc[0])
        if votos < 2000:
            return f"La película '{titulo_de_la_filmacion}' fue estrenada en el año {pelicula['release_date'].dt.year.iloc[0]}. La misma cuenta con menos de 2000 valoraciones."
        else:
            titulo_original = pelicula['title'].iloc[0]
            promedio = round(pelicula['popularity'].iloc[0], 2)
            return f"La película '{titulo_original}' fue estrenada en el año {pelicula['release_date'].dt.year.iloc[0]}. Tiene un total de {votos} valoraciones, con un promedio de {promedio}."

@app.get("/actor/{Actor}")

def get_actor(nombre_actor:str):
    nombre_actor_lower = nombre_actor.lower()
    peliculas_actor = df_movies[df_movies['actors'].str.lower().str.contains(nombre_actor_lower, na=False) &
        (~df_movies['director'].str.lower().str.contains(nombre_actor_lower, na=False))]
    if peliculas_actor.empty:
        return f"No se encontró información para el actor '{nombre_actor}'."
    else:
        cantidad_peliculas = len(peliculas_actor)
        retorno_promedio = peliculas_actor['return'].mean()
        return f"{nombre_actor} ha participado en {cantidad_peliculas} {'filmaciones' if cantidad_peliculas != 1 else 'filmación'}, con un retorno promedio de ${retorno_promedio:.2f}."


@app.get("/director/{Director}")

def get_director(nombre_director:str):
    df_movies['release_date']= pd.to_datetime(df_movies['release_date'],format= '%Y-%m-%d')
    nombre_director_lower = nombre_director.lower()
    peliculas_director = df_movies[df_movies['director'].str.lower().str.contains(nombre_director_lower, na=False)]
    if peliculas_director.empty:
        return f"No se encontró información para el director '{nombre_director}'."
    else:
        cantidad_peliculas = len(peliculas_director)
        retorno_total = round(peliculas_director['return'].sum(), 2)
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
    
@app.get("/recommend/{Recomendarpelículas}", response_model=List[str])  

def recomendacion(titulo: str):
    titulo = titulo.lower()
    titulo_pelicula = df_recommend[df_recommend['title'].str.lower() == titulo]

    if titulo_pelicula.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró la película {titulo}")

    indice_producto = titulo_pelicula.index[0]
    similitudes_producto = cosine_matrix[indice_producto]
    indices_top_5_similares = np.argsort(-similitudes_producto)[1:6]
    top_5_peliculas = df_recommend.loc[indices_top_5_similares, 'title'].tolist()  # Convierte a lista
<<<<<<< HEAD
    return top_5_peliculas # print(f"Películas similares a {titulo.capitalize()} son:{top_5_peliculas}")
=======
    return top_5_peliculas
>>>>>>> e0af8d68828f6f5576a3021aa56179a16c34b203
