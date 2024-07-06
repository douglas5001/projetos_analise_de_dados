import pandas as pd


def extract_data():
    data = pd.read_csv('usuarios.csv')
    df = pd.DataFrame(data)
    return df

