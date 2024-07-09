from ETL.extract import extract_data
from ETL.transform import transform_data
from ETL.load import load_data

def run_pipeline():
    print('Starting ETL...')

    # Extraction
    data = extract_data()

    # Transformation
    df = transform_data(data)

    # Load
    load_data(df)

    print('ETL finished')

if __name__ == "__main__":
    run_pipeline()