from fastapi import FastAPI
import pandas as pd
import ast
import pickle
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error
from functions import obtener_top_genero


app = FastAPI()

#------Lectura------

df2 = pd.read_json('steam_games2.json', encoding='utf-8')
df2.to_csv('steam_games_limpio.csv')
df = pd.read_csv('steam_games_limpio.csv', encoding='utf-8')

#------Limpieza------

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df.drop('Unnamed: 0', axis=1,inplace=True)

#------General------

def filtrar_año(Año):
    return df[df['release_date'].dt.year == int(Año)]

#------API------
def obtener_top_genero(Año):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['genres'])
    df_filtered['genres'] = df_filtered['genres'].apply(ast.literal_eval)
    all_genres = [genre for sublist in df_filtered['genres'] for genre in sublist]
    genre_counts = pd.Series(all_genres).value_counts()
    top_genres_dict = genre_counts.head(5).to_dict()
    return top_genres_dict

def obtener_juego(Año):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['app_name'])
    return df_filtered['app_name']


def obtener_top_specs(Año):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['specs'])
    df_filtered['specs'] = df_filtered['specs'].apply(ast.literal_eval)
    all_specs = [specs for sublist in df_filtered['specs'] for specs in sublist]
    specs_counts = pd.Series(all_specs).value_counts()
    top_specs_dict = specs_counts.head(5).to_dict()

    return top_specs_dict

def obtener_suma_early_access(Año):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['early_access'])
    cantidad_early_access = df_filtered['early_access'].sum()
    cantidad_early_access = int(cantidad_early_access)
    
    return cantidad_early_access

def obtener_sentiment(Año: str):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['sentiment'])
    df_filtered = df_filtered[~df_filtered['sentiment'].str.contains('user reviews')]
    sentiment_counts = df_filtered['sentiment'].value_counts()
    sentiment_dict = sentiment_counts.to_dict()
    
    return sentiment_dict

def obtener_top_metascore(Año: str):
    df_filtered = df[df['release_date'].dt.year == int(Año)]
    df_filtered = df_filtered.dropna(subset=['metascore'])
    df_sorted = df_filtered.sort_values(by='metascore', ascending=False)
    top_5_games = df_sorted.head(5)
    juegos_y_metascore = dict(zip(top_5_games['title'], top_5_games['metascore']))
    return juegos_y_metascore

def predecir_precio_y_rmse(generos, early_access):
    data = joblib.load('modelo.pkl')
    modelo_regresion = data['modelo']
    poly = data['poly']
    X_test_poly = data['X_test_poly']
    y_test = data['y_test']
    X = data['X']

    generos_a_predecir_df = pd.DataFrame({genero: [1 if genero in generos else 0] for genero in X.columns})


    generos_a_predecir_df['early_access'] = int(early_access)


    generos_a_predecir_poly = poly.transform(generos_a_predecir_df)


    precio_predicho = modelo_regresion.predict(generos_a_predecir_poly)[0]

    y_pred = modelo_regresion.predict(X_test_poly)
    mse = mean_squared_error(y_test, y_pred)

    rmse = np.sqrt(mse)

    return precio_predicho, rmse

#------API------

@app.get('/genero')
def genero(Año: str):
    return obtener_top_genero(Año)

@app.get('/juegos')
def juegos(Año: str):
    return obtener_juego(Año)

@app.get('/specs')
def specs(Año: str):
    return obtener_top_specs(Año)

@app.get('/earlyaccess')
def earlyacces(Año:str):  
    return obtener_suma_early_access(Año)

@app.get('/sentiment')
def sentiment(Año: str):
    return obtener_sentiment(Año)

@app.get('/metascore')
def metascore(Año: str):
    return obtener_top_metascore(Año)

@app.get('/predecir')
def predecir_endpoint(generos: str, early_access: bool):
    generos_pred, early_access_pred = predecir_precio_y_rmse(generos, early_access)
    
    response = {
        'precio_predicho': round(generos_pred, 2),
        'RMSE': round(early_access_pred, 2)
    }
    return response

print(predecir_precio_y_rmse('Indie', True))