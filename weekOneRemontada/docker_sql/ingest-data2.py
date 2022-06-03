import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user=params.user
    password=params.password
    host=params.host
    url=params.url
    port=params.port
    table_name=params.table_name
    db=params.db

    csv_name='taxi_zone_lookup.csv'
    os.system(f"wget {url} -O {csv_name}")

    engine=create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    df_iter=pd.read_csv(csv_name,iterator=True,chunksize=100)

    df=next(df_iter)

    df.head(n=0).to_sql(name=table_name,con=engine,if_exists='replace')

    df.to_sql(name=table_name,con=engine,if_exists='append')

    for data in df_iter:
        t_start=time()
        data.to_sql(name=table_name,con=engine,if_exists='append')
        t_end=time()

        print(f'Inserted another chunk... Time in Seconds: {t_end-t_start}')
    
if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Ingest More CSV data to Postgres')

    # add arguments
    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database name for postgres')
    parser.add_argument('--table_name',help='name of the table where we write results to')
    parser.add_argument('--url',help='url location of the CSV file')

    args=parser.parse_args()

    main(args)