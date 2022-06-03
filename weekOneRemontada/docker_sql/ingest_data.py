import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    table_name=params.table_name
    url=params.url

    csv_name='output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine=create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    engine.connect()

    df_iter=pd.read_csv(csv_name,iterator=True,chunksize=100000)


    df=next(df_iter)


    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)


    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')


    for data in df_iter:
        t_start=time()
        data.tpep_pickup_datetime=pd.to_datetime(data.tpep_pickup_datetime)
        data.tpep_dropoff_datetime=pd.to_datetime(data.tpep_dropoff_datetime)
        
        data.to_sql(name=table_name,con=engine,if_exists='append')
        
        t_end=time()
        
        print(f'Inserted another chunk... Time in Seconds: {t_end-t_start}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # add arguments
    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--table-name',help='name of the table where we write results to')
    parser.add_argument('--url',help='url location of the CSV file')

    args=parser.parse_args()

    main(args)




