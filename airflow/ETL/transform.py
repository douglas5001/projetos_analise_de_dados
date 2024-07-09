# src/transform.py

import pandas as pd
from datetime import datetime

def transform_data(df):
    df_cols = pd.DataFrame(columns=['userId', 'id', 'title', 'body'])
    df_data = pd.concat([df_cols, df], ignore_index=True, join='inner')

    df_data = df_data.rename({
        'userId': 'userid',
        'id': 'id',
        'title': 'title',
        'body':'body'
    }, axis=1)

    df_data = df_data.astype('string')
    df_data['inserted_at'] = datetime.now()
    #df_data['cpf'] = df_data['cpf'].str.replace('.', '', regex=False).str.replace('-', '', regex=False)

    return df_data
