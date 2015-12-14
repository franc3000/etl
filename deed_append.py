#!/usr/bin/env python2.7

import logging
import luigi
import config
from db import get_db, execute
from db_table_target import DbTableTarget
from load_clean import LoadCleanDeeds

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


class DeedAppend(luigi.Task):
    log = logging.getLogger(__name__)
    db = get_db()

    def __init__(self):
        super(DeedAppend, self).__init__()
        self.appendtables = []

    def requires(self):
        return LoadCleanDeeds()

    def run(self):
        self.cleantables = map(lambda t: t.tablename, self.input())

        for table in self.cleantables:
            appendtable = table + '_append'
            self._run_sql(table, appendtable)
            self.appendtables.append(appendtable)

    def output(self):
        return map(DbTableTarget, self.appendtables)

    def _run_sql(self, oldtable, newtable):
        fp = open('deed_append.sql')
        sql = fp.read()
        fp.close()

        sql = sql.replace('[DEED_CLEAN_TABLE]', oldtable)
        sql = sql.replace('[DEED_APPEND_TABLE]', newtable)

        execute(sql)
