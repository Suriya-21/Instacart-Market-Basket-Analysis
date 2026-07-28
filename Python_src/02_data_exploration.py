import pandas as pd
from config import engine
from utils.database import load_transactions

df = load_transactions(500000)

print(df.head())

print(df.shape)

print(df.info())

print(df.describe(include="all"))