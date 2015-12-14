#!/usr/bin/env python2.7

from sqlalchemy import create_engine, text
import config

db = None


def get_db():
    """Get database connection"""
    global db
    db = db or create_engine('mysql://' +
                             config.DB_USERNAME + ':' + config.DB_PASSWORD +
                             '@' + config.DB_URL + ':' + config.DB_PORT +
                             '/' + config.DB_NAME)
    assert db is not None
    return db


def execute(sql):
    # split SQL into multiple lines and remove blanks
    # sql_statements = filter(lambda s: s.strip() != '', sql.split(';'))

    f = open('log.sql', 'w')
    f.write(sql)
    f.close()

    return db.execute(text(sql))
    # for stmt in sql_statements:
    #    db.execute(text(stmt))
