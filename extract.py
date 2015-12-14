#!/usr/bin/env python2.7

import sys
import logging

import luigi
from boto.s3.connection import S3Connection

import config

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


class ExtractDeeds(luigi.Task):
    log = logging.getLogger(__name__)

    bucket_name = luigi.Parameter(default=config.BUCKET_NAME)
    key_name = luigi.Parameter(default=config.KEY_NAME)

    def __init__(self):
        self.filenames = []
        luigi.Task.__init__(self)

    def run(self):
        csv_keys = self._get_csv_keys()
        for key in csv_keys:
            key_filename = self._save_file(key)
            self.filenames.append(key_filename)

    def output(self):
        """CSV filenames"""
        return map(luigi.LocalTarget, self.filenames)

    def _get_csv_keys(self):
        """Returns list of S3 keys for the given S3 bucket and key name"""
        bucket_name = self.bucket_name
        key_name = self.key_name

        conn = S3Connection(config.ACCESS_KEY, config.SECRET_ACCESS_KEY)
        try:
            bucket = conn.get_bucket(bucket_name)
        except Exception as e:
            self.log.critical('Could not access S3 bucket: ' + bucket_name +
                              '\n' + e)
            sys.exit()

        try:
            all_keys = bucket.get_all_keys(prefix=key_name)
            csv_keys = filter(lambda key: key.name.endswith('.csv'), all_keys)
        except Exception as e:
            self.log.critical('Could not access key: ' + key_name +
                              ' on bucket: ' + bucket_name +
                              '\n' + e)
            sys.exit()

        if len(csv_keys) < 1:
            self.log.error('No CSV files in bucket ' + bucket_name +
                           ' with prefix ' + key_name)

        return csv_keys

    def _save_file(self, key):
        """Saves file from S3 bucket key and returns the filename"""
        key_filename = key.name.split('/')[1]
        fp = open(key_filename, 'w')
        key.get_file(fp)
        fp.close()
        return key_filename
