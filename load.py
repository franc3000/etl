#!/usr/bin/env python2.7

import os
import logging

import luigi
import pandas as pd

import config
from db import get_db
from db_table_target import DbTableTarget
from extract import ExtractDeeds

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


class LoadDeeds(luigi.Task):
    log = logging.getLogger(__name__)
    db = get_db()

    def __init__(self):
        super(LoadDeeds, self).__init__()
        self.tablenames = []  # DB tables that were successfully created

    def requires(self):
        return ExtractDeeds()

    def run(self):
        csv_filepaths = map(lambda target: target.path, self.input())

        for csvfile in csv_filepaths:
            df = self._load_csv_into_dataframe(csvfile)
            tablename = csvfile.rstrip('.csv')
            try:
                self._load_dataframe_into_db(df, tablename)
            except Exception as e:
                self.log.critical('Failed to load: ' + csvfile + ' into DB' +
                                  '\n' + e)
            else:
                os.remove(csvfile)  # clean up if data was successfully loaded
                self.tablenames.append(tablename)

    def output(self):
        """Returns DB table names"""
        return map(DbTableTarget, self.tablenames)

    def _load_csv_into_dataframe(self, csvfile):
        df = pd.read_csv(csvfile, header=0)
        df.rename(columns=self._clean_dataframe_column, inplace=True)
        return df

    def _clean_dataframe_column(self, colname):
        """Lowercase column name, replace/remove special characters"""
        colname = str.lower(colname)
        colname = colname.replace('%', 'pct')
        colname = colname.replace('+', 'plus')
        colname = colname.replace(' ', '_')
        colname = colname.replace('.', '_')
        colname = colname.replace(':', '_')
        colname = colname.replace('/', '_')
        colname = colname.replace('(', '')
        colname = colname.replace(')', '')
        colname = colname.replace('-', '_')
        colname = colname.replace('__', '_')
        colname = colname.replace('__', '_')

        # remove chars
        colname = colname.replace('#', '')
        colname = colname.replace('&_', '')

        return colname

    def _load_dataframe_into_db(self, df, tablename):
        db = self.db
        df.to_sql(name=tablename, con=db, flavor='mysql',
                  if_exists='replace', index=False, chunksize=250)
