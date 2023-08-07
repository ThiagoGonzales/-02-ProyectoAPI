from fastapi import FastAPI
from functions import *

app = FastAPI()

#------API------

@app.get('/genero/{Año}')
def genero(Año: str):
    return obtener_top_genero(Año)

@app.get('/juegos/{Año}')
def juegos(Año: str):
    return filtrar_año(Año)

@app.get('/specs/{Año}')
def specs(Año: str):
    return obtener_top_specs(Año)

@app.get('/early_access/{Año}')
def early_access(Año: str):
    return obtener_suma_early_access(Año)

@app.get('/sentiment/{Año}')
def sentiment(Año: str):
    return obtener_sentiment(Año)

@app.get('/metascore/{Año}')
def metascore(Año: str):
    return obtener_top_metascore(Año)