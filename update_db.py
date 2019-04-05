#!/usr/bin/python
import psycopg2
from config import config
from create_data import etf_data_list

def insert_etf_data():
    """ Connect to PostgreSQL server """
    conn = None
    try:
        params = config()

        print('Connecting to PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        
        data = etf_data_list()
        for entry in data:
            [name, kind, isin, price, currency] = entry
            cur.execute('INSERT INTO prices (name, kind, isin, price, currency) VALUES (%s, %s, %s, %s, %s)', (name, kind, isin, price, currency))
        conn.commit() 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    insert_etf_data()
