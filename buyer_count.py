#!/usr/bin/env python2.7

import logging
import luigi
import config
from db import get_db, execute
from db_table_target import DbTableTarget
from load_clean import LoadCleanDeeds

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


class BuyerCount(luigi.Task):
    log = logging.getLogger(__name__)
    db = get_db()

    def __init__(self):
        super(BuyerCount, self).__init__()
        self.buyercounttables = []

    def requires(self):
        return LoadCleanDeeds()

    def run(self):
        self.cleantables = map(lambda t: t.tablename, self.input())

        for table in self.cleantables:
            buyercount = table + '_buyercount'
            self._run_sql(table, buyercount)
            self.buyercounttables.append(buyercount)

    def output(self):
        return map(DbTableTarget, self.buyercounttables)

    def _run_sql(self, oldtable, newtable):
        fp = open('buyer_count.sql')
        sql = fp.read()
        fp.close()

        sql = sql.replace('[DEED_CLEAN_TABLE]', oldtable)
        sql = sql.replace('[BUYER_COUNT_TABLE]', newtable)

        execute(sql)
