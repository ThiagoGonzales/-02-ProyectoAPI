import pandas as pd

#------Lectura------

df = pd.read_json(r'datos\\steam_games2.json')

#------Limpieza------

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

#------General------

def filtrar_año(Año):
    return df[df['release_date'].dt.year == Año]

#------API------

def obtener_top_genero(Año):
    df_año = filtrar_año(Año)
    df_año = df_año.dropna(subset=['genres'])
    genres = [spec for sublist in df_año['genres'] for spec in sublist]
    top_5 = pd.Series(genres).value_counts().head(5).to_dict()
    return top_5

def obtener_top_specs(Año):
    df_año = filtrar_año(Año)
    df_año = df_año.dropna(subset=['specs'])
    specs = [spec for sublist in df_año['specs'] for spec in sublist]
    top_5 = pd.Series(specs).value_counts().head(5).to_dict()
    return top_5

def obtener_suma_early_access(Año):
    df_año = filtrar_año(Año)
    suma = df_año['early_access'].sum()
    return suma

def obtener_sentiment(Año: str):
    df_año = filtrar_año(Año)
    sentiment_fil = ['Positive', 'Mixed', 'Very Positive', 'Mostly Positive', 'Mostly Negative', 'Overwhelmingly Positive', 'Negative', 'Very Negative']
    df_fil = df_año['sentiment'].value_counts()[sentiment_fil].to_dict()
    return df_fil

def obtener_top_metascore(Año: str):
    df_año = filtrar_año(Año)
    top_5 = df_año.sort_values(by='metascore', ascending=False)
    return top_5.head(5)

#------