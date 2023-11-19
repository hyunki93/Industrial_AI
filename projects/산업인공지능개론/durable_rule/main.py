import psycopg2
from datetime import datetime, timedelta
from durable.lang import *


def db_query():
    conn = psycopg2.connect(
        host="210.217.8.204",
        port="21002",
        database="tadb",
        user="tauser",
        password="ryxhd!@#$"
    )
    cursor = conn.cursor()
    query = "SELECT * FROM public.bucheon_collect_hist ORDER BY collect_dt DESC LIMIT 1"
    cursor.execute(query)
    data = cursor.fetchone()
    conn.close()
    return data


def check_data_rule(c):
    @when_all(c.db_data.timestamp < datetime.now() - timedelta(minutes=5))
    def alert(c):
        print("Data collection has not occurred for more than 5 minutes!")


if __name__ == '__main__':
    with ruleset('data_check'):
        db_data = db_query()
        check_data_rule({'db_data': db_data})
    post('data_check', {'db_data': db_data})
