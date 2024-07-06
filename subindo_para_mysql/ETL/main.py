import pandas as pd
from ETL.extract import extract_data
from ETL.transform import transform_data
from ETL.load import load_data

print('Iniciando ETL..')

# Extração de dados
data = extract_data()

# Transformação de dados
df = transform_data(data)

# Carregamento de dados
load_data(df)

print('ETL encerrado')
