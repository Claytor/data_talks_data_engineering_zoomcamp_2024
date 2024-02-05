#!/usr/bin/env python
# coding: utf-8

# Imports
import os
import argparse
from time import time
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Main method accepts arguments that were parsed below 
def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    parquet_name = 'data/output.parquet'
    url = params.url

    # Ensure the target directory exists
    os.makedirs(os.path.dirname(parquet_name), exist_ok=True)
    
    # Download the parquet with wget and output to file named 'parquet_name'
    try:
        print('Downloading file')
        os.system(f'wget {url} -O {parquet_name}')
    except Exception as e:
        print(f'Error downloading the file: {e}')
        return

    # Create an engine
    try:
        print('Connecting to database')
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    except SQLAlchemyError as e:
        printprint(f'Error connecting to the database: {e}')
        return
    
    # Read data
    try:
        print("Reading parquet file")
        df = pd.read_parquet(parquet_name)
    except Exception as e:
        print(f'Error reading the parquet file: {e}')
        return
    
    # Write head and data to sql database
    try:
        print('Writing to database')
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')
    except SQLAlchemyError as e:
        print(f'Error writing to the database: {e}')

if __name__ == '__main__':
    # parser variable from argparse accepts arguments and we pass them to the args variable 
    parser = argparse.ArgumentParser(description='Ingest parquet data to Postgres.')
   
    # add arguments to be parsed
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--table_name', help='name of table we will write results to')
    parser.add_argument('--url', help='url of the parquet file')
   
    # args variable accepts all parsed arguments
    args = parser.parse_args()
   
    # pass arguments to the main method
    main(args)