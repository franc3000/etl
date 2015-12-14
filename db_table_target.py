#!/usr/bin/env python2.7

import luigi
from db import get_db


class DbTableTarget(luigi.Target):
    """Database Table Target for Luigi"""

    def __init__(self, tablename):
        self.tablename = tablename

    def exists(self):
        db = get_db()
        sql = 'SHOW TABLES LIKE "' + self.tablename + '"'
        return db.scalar(sql) is not None
