from sqlite3 import IntegrityError

from sqlalchemy import create_engine, event, text
from urllib.parse import quote_plus


def encontrar_palavra_no_arquivo(nome_arquivo, palavra_procurada):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        for numero_linha, linha in enumerate(linhas, start=1):
            if palavra_procurada in linha:
                print(f"Palavra '{palavra_procurada}' encontrada na linha {numero_linha}: {linha.strip()}")
    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")



def sqlConnector():
    
    with open('tegras.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    for numero_linha, linha in enumerate(linhas, start=1):
        if 'host:' in linha:
            linha = linha.replace('host: ', '')
            linha = linha.replace('\n', '')
            server = linha
        elif 'database:' in linha:
            linha = linha.replace('database: ', '')
            linha = linha.replace('\n', '')
            database = linha
        elif 'user:' in linha:
            linha = linha.replace('user: ', '')
            linha = linha.replace('\n', '')
            username = linha
        elif 'password:' in linha:
            linha = linha.replace('password: ', '')
            linha = linha.replace('\n', '')
            password = linha
            
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{server}:3306/{database}')

    return engine


def load_data(df_data):
    try:
        table_name = 'usuario'
        schema = 'python_sql'
        engine = sqlConnector()
        df_data.to_sql(name=table_name, index=False, con=engine, schema=schema, if_exists='append', method='multi',
                       chunksize=((2100 // len(df_data.columns)) - 1))
        print(f'inserted into {schema}.{table_name}')
    except Exception as e:
        print('Erro ao carregar dados no banco: ', e)

    try:
        engine = sqlConnector()
        conn = engine.connect()
        conn.execute(text(f"""
                            DELETE t
                            FROM {schema}.{table_name} t
                            LEFT JOIN (
                                SELECT cpf, MAX(inserted_at) AS max_data
                                FROM {schema}.{table_name}
                                GROUP BY cpf
                            ) cte
                            ON t.cpf = cte.cpf AND t.inserted_at <> cte.max_data
                            WHERE cte.cpf IS NOT NULL
                            """))
        conn.commit()
        conn.close()
        print('Dados deduplicados com sucesso.')
    except Exception as e:
        print('Erro ao deduplicar dados: ', e)

    # try:
    #     engine = sqlConnector()
    #     with engine.begin() as conn:
    #         conn.execute(text(f"""DELETE FROM {schema}.{table_name}
    #                             WHERE (cpf, inserted_at) NOT IN (
    #                                 SELECT cpf, MAX(inserted_at) AS max_data
    #                                 FROM {schema}.{table_name}
    #                                 GROUP BY cpf
    #                             );"""))
    #     print('Deduplicated records in the database')
    # except Exception as e:
    #     print('Erro ao deduplicar dados: ', e)