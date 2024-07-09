from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def sqlConnector():
    
    server = os.getenv('HOST')
    database = os.getenv('DATABASE')
    username = os.getenv('USER')
    password = os.getenv('PASSWORD')

    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{server}:5432/{database}')
    return engine

def load_data(df_data):
    table_name = 'usuario'
    schema = 'usuarios'

    try:
        engine = sqlConnector()
        df_data.to_sql(name=table_name, index=False, con=engine, schema=schema, if_exists='append', method='multi',
                       chunksize=((2100 // len(df_data.columns)) - 1))
        print(f'Inserted into {schema}.{table_name}')
    except Exception as e:
        print('Error loading data into the database:', e)

    try:
        engine = sqlConnector()
        with engine.connect() as conn:
            conn.execute(text(f"""
                DELETE FROM {schema}.{table_name} t
                USING (
                    SELECT userid, MAX(inserted_at) AS max_data
                    FROM {schema}.{table_name}
                    GROUP BY userid
                ) cte
                WHERE t.userid = cte.userid AND t.inserted_at <> cte.max_data
            """))
        print('Data deduplication completed successfully.')
        conn.commit()
        conn.close()
    except Exception as e:
        print('Error deduplicating data:', e)
