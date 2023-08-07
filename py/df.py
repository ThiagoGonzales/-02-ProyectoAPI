import pandas as pd
import ast

rows = []
with open(r'datos\\steam_games.json') as f:
    for line in f.readlines():
        rows.append(ast.literal_eval(line))

df = pd.DataFrame(rows)

df.to_json(r'datos\\steam_games3.json')