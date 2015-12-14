#!/usr/bin/env python2.7
import coloredlogs
import logging
coloredlogs.install()

# Amazon Config
ACCESS_KEY = 'AKIAIJRD45NMHVNQQPWA'
SECRET_ACCESS_KEY = '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'
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
