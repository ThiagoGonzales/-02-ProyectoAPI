from functions import *
import pandas as pd
import ast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

#------Limpieza------

df_ml = df

df_ml.dropna(subset=['genres'], inplace=True)

# Convertir la columna 'price' a tipo numerico y eliminar filas con valores faltantes en 'price'
df_ml['price'] = pd.to_numeric(df_ml['price'], errors='coerce')
df_ml.dropna(subset=['price'], inplace=True)

# Eliminar duplicados 
df_ml.drop_duplicates(subset='id',inplace=True)

# Eliminar columnas no útiles
colum = ['publisher','app_name','title','url','release_date','tags','discount_price','reviews_url','specs','id','developer','sentiment','metascore']
df_ml.drop(colum, axis=1, inplace=True)

#------Maching learning------

# Deshacer las listas
df_exploded = df_ml.explode('genres')

# Crear columnas dummy
df_dummies = pd.get_dummies(df_exploded['genres'])

# Agregar la columna 'price' y 'ACCESO_ANTISIPADO' al DataFrame df_dummies
df_dummies['price'] = df_exploded['price']
df_dummies['early_access'] = df_exploded['early_access']

# Agrupar por el índice (género) y sumar las filas agrupadas
df_grouped = df_dummies.groupby(df_dummies.index).sum()

# Agregar las columnas 'price' y 'early_access' después del groupby
df_grouped['price'] = df_exploded.groupby(df_exploded.index).first()['price']
df_grouped['early_access'] = df_exploded.groupby(df_exploded.index).first()['early_access']

# Reemplazar df2 con el DataFrame final df_grouped
df_ml = df_grouped

df_ml = df_ml[df_ml['price'] != 0.00]
df_ml = df_ml[df_ml['Free to Play'] != 1]
df_ml = df_ml.drop('Free to Play', axis=1)

X = df_ml.drop(columns=['price', 'Early Access'], axis=1)
y = df_ml['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Especificar el grado del polinomio deseado
grado_polinomio = 1

# Crea el transformador polinomial
poly = PolynomialFeatures(degree=grado_polinomio)

X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

modelo_regresion = LinearRegression()

# Entrena el modelo utilizando las características polinomiales
modelo_regresion.fit(X_train_poly, y_train)

# Realiza predicciones en el conjunto de prueba
y_pred = modelo_regresion.predict(X_test_poly)

# Calcular el Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)

# Calcular el Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)

import pickle
# Guardar el modelo, X_test_poly, y_test y y_pred en un archivo pkl
data_to_save = {'modelo': modelo_regresion, 'X_test_poly': X_test_poly, 'y_test': y_test, 'y_pred': y_pred, 'poly': poly, 'X': X}

with open('modelo.pkl', 'wb') as file:
    pickle.dump(data_to_save, file)

import joblib
def predecir_precio_y_rmse(generos, early_access):
    # Cargar el modelo y los datos desde el archivo pkl
    data = joblib.load('modelo.pkl')
    modelo_regresion = data['modelo']
    poly = data['poly']
    X_test_poly = data['X_test_poly']
    y_test = data['y_test']

    # Crear un DataFrame con las características de los géneros a predecir
    generos_a_predecir_df = pd.DataFrame({genero: [1 if genero in generos else 0] for genero in X.columns})

    # Agregar la columna 'early_access' al DataFrame con el valor proporcionado por el usuario
    generos_a_predecir_df['early_access'] = int(early_access)

    # Transformar las características de los géneros a predecir utilizando el mismo transformador polinomial
    generos_a_predecir_poly = poly.transform(generos_a_predecir_df)

    # Realizar la predicción utilizando el modelo cargado
    precio_predicho = modelo_regresion.predict(generos_a_predecir_poly)[0]

    # Calcular el Mean Squared Error (MSE)
    y_pred = modelo_regresion.predict(X_test_poly)
    mse = mean_squared_error(y_test, y_pred)

    # Calcular el Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)

    return precio_predicho, rmse

# Ejemplo de uso:
generos_a_predecir = ['Utilities']
early_access = True
precio_predicho, rmse = predecir_precio_y_rmse(generos_a_predecir, early_access)
print(f"Precio predicho: {round(precio_predicho, 2)}")
print(f"RMSE: {rmse}")