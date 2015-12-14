#!/usr/bin/env python2.7

import sys
import config
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def get_csv_keys(bucket_name=config.BUCKET_NAME, key_name=config.KEY_NAME):
    """Returns list of S3 keys for the given S3 bucket and key name"""
    conn = S3Connection(config.ACCESS_KEY, config.SECRET_ACCESS_KEY)
    try:
        bucket = conn.get_bucket(bucket_name)
    except Exception as e:
        print 'Could not access S3 bucket:', bucket_name, '\n' + e
        sys.exit()

    try:
        #keys = bucket.list(key_name)
        all_keys = bucket.get_all_keys(prefix=key_name)
        csv_keys = filter(lambda key: key.name.endswith('.csv'), all_keys)
    except Exception as e:
        print 'Could not access key:', key_name, 'on bucket:', bucket_name, '\n' + e
        sys.exit()

    if len(csv_keys) < 1:
        print 'WARNING: Did not find any CSV files in bucket', bucket_name, 'with prefix', key_name

    return csv_keys


import pandas as pd
from sqlalchemy import create_engine

def _save_file(key):
    """Saves file from S3 bucket key and returns the filename"""
    # save file
    key_filename = key.name.split('/')[1]
    fp = open(key_filename, 'w')
    key.get_file(fp)
    fp.close()
    return key_filename

def dataframes_from_csvs(keys):
    """Takes S3 keys and loads them into pandas dataframe"""
    dataframes = []
    for key in keys:
        key_filename = _save_file(key)
        df = pd.read_csv(key_filename, header=0)
        dataframes.append(df)

    return dataframes

def _get_db_connection():
    return create_engine('mysql://' +
                         config.DB_USERNAME + ':' + config.DB_PASSWORD +
                         '@' + config.DB_URL + ':' + config.DB_PORT +
                         '/' + config.DB_NAME)

def load_dataframes_into_db(dataframes, table_name=config.TABLE_NAME):
    """Connect to RDS MySQL Database (specified in config) and load pandas dataframes. Returns SQLAlchemy db engine/connection in case you want to use it"""
    #rds = boto.rds2.connect_to_region(config.REGION_NAME)
    db = _get_db_connection()
    for df in dataframes:
        df.to_sql(name=table_name, con=db, flavor='mysql', if_exists='append', index=False, chunksize=250)
        if db.scalar("SELECT ROW_COUNT();") < 1:
            print "WARNING: did not insert rows for current dataframe"
            print "Current dataframe shape:", df.shape # For identifying which dataframe it was
    return db

def transform_db_data():
    pass

def main():
    csv_keys = get_csv_keys()
    dataframes = dataframes_from_csvs(csv_keys)
    db = load_dataframes_into_db(dataframes)

if __name__ == '__main__':
    main()
