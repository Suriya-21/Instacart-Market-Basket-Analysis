import pandas as pd
from config import engine

query = "SELECT version();"

df = pd.read_sql(query, engine)

print(df)