from datetime import datetime
import pandas as pd
#from unidecode import unidecode


def transform_data(df):

    df_cols = pd.DataFrame(columns=['Nome', 'Email', 'CPF'])

    df_data = pd.concat([df_cols, df], ignore_index=True, join='inner')

    df_data = df_data.rename({
        'Nome':'nome',
        'Email':'email',
        'CPF':'cpf'
    }, axis=1)

    df_data = df_data.astype('string')
    df_data['inserted_at'] = datetime.now()

    df_data['cpf'] = df_data['cpf'].str.replace('.', '', regex=False).str.replace('-', '', regex=False)

    #df_data = df_data.where(pd.notnull(df_data), None)

    return df_data
