import psycopg2


def connect():
    conn = psycopg2.connect(host='localhost', database='autofuzz',
                            user='postgres', password='ct12345678')
    return conn
