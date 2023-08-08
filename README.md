

# Proyecto Individual 1

![Steam](https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2023/06/Steam.jpg?w=1500&quality=82&strip=all&ssl=1)

### El proyecto tiene como objetivo analizar el conjunto de datos de todos los juegos y aplicaciones de Steam desde 1970 hasta 2021.

## ETL

- Cambiar de distribución el archivo steam_games.json y renombrarlo a steam_games2.json

- Eliminar filas con años incorrectos  
- Eliminar Duplicados
- En cada caso particular eliminar datos nulos

## EDA 

- Para lograr el objetivo de predecir el precio de un juego tomé en cuentas las columnas `genres`, `early_access` y `price`, descartando a las demás para que el dataframe queda así.
|genres                                       |price|early_access|
|---------------------------------------------|-----|------------|
|[Action, Casual, Indie, Simulation, Strategy]|4.99 |False       |
|[Action, Adventure, Casual]	              |0.99 |False       |
|[Action, Adventure, Simulation]              |3.99 |False       |
|[Free to Play, Indie, Simulation, Sports]    |9.99 |False       |
|[Free to Play, Indie, Simulation, Sports]    |18.99|False       |

- Con estos datos luego cree un grafico del promedio de los precios de los juegos separados por los generos.
![graph](https://i.imgur.com/HuxRrVU.png)

 aquí vemos que los productos de `Animation & modeling`, `Video Production` y `Educatión`  son los más costosos, mientras que los precios de juegos con generos de `Action`, `Indie` y `Casual` son los más baratos.

- Luego cree un dataframe con columnas de todos los generos separados (dummies) y early_access

|Utilities|Strategy|early_access|
|---------|--------|------------|
|        1|       0|       False|       
|        0|       1|       False|    
|        0|       0|       False|    
|        0|       0|       False|    
|        1|       1|       False| 

Ejemplo de como quedarían

- Estos datos ya están listos para empezar a entrenar  el modelo.

## EndPoints

- `genero(Año: str):` Retorna un diccionario con los 5 géneros de juegos más ofrecidos en el año indicado.

- `juegos(Año: str):` Retorna una lista de juegos lanzados en el año indicado.

- `specs(Año: str):` Retorna una lista con los cinco specs más comunes que se repiten en el año indicado.

- `early_access(año: str):` Retorna la cantidad de juegos lanzados en early access durante el año indicado.

- `sentiment(Año: str)`: Retorna el número de registros categorizados mediante un análisis de sentimiento durante el añ` indicado.

- `metascore(Año: str)`: Retorna una lista con los cinco juegos mejor calificados según el metascore durante el año indicado.




