#!/usr/bin/env python2.7
import csv
import coloredlogs
import logging
coloredlogs.install()

# Amazon Config
# read in the credentials file
with open('credentials.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row['User Name'], row['Access Key Id'], row['Secret Access Key'])
        ACCESS_KEY = row['Access Key Id']
        SECRET_ACCESS_KEY = row['Secret Access Key']

REGION_NAME = 'us-west-2'

# Amazon S3
BUCKET_NAME = 'pareto-public'
KEY_NAME = 'deed/'

# Amazon RDS MySQL Database
# mysql://awstesting:qwertyui@testing.cc5mu8tdrn2i.us-west-2.rds.amazonaws.com:3306/test
DB_URL = 'testing.cc5mu8tdrn2i.us-west-2.rds.amazonaws.com'
DB_PORT = '3306'
DB_USERNAME = 'awstesting'
DB_PASSWORD = 'qwertyui'
DB_NAME = 'test'

LOG_FORMAT = '%(asctime)s -  %(levelname)s - %(message)s'
LOG_LEVEL = logging.WARN
