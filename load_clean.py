#!/usr/bin/env python2.7

import logging
import luigi
import config
from db import get_db, execute
from db_table_target import DbTableTarget
from load import LoadDeeds

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


class LoadCleanDeeds(luigi.Task):
    log = logging.getLogger(__name__)
    db = get_db()

    def __init__(self):
        super(LoadCleanDeeds, self).__init__()
        self.cleantables = []

    def requires(self):
        return LoadDeeds()

    def run(self):
        self.tables = map(lambda t: t.tablename, self.input())

        for table in self.tables:
            cleantable = table + '_clean'
            self._run_sql(table, cleantable)
            self.cleantables.append(cleantable)

    def output(self):
        return map(DbTableTarget, self.cleantables)

    def _run_sql(self, oldtable, newtable):
        fp = open('deed_clean.sql')
        sql = fp.read()
        fp.close()

        sql = sql.replace('[DEED_TABLE]', oldtable)
        sql = sql.replace('[DEED_CLEAN_TABLE]', newtable)

        execute(sql)
