import psycopg2, datetime


def connect():
    # conn = psycopg2.connect(host='localhost', database='autofuzz',
                            # user='postgres', password='ct12345678')
    conn = psycopg2.connect(host='localhost', database='demo',
                            user='postgres', password='ct12345678')
    return conn

def select(sql: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    conn.close()
    return rst

def generate_fid():
    # generate fid
    conn = connect()
    cur = conn.cursor()
    sql = """select max("fid") from "file";"""
    cur.execute(sql)
    max_fid = cur.fetchone()[0]
    if max_fid is None:
        fid = 1
    else:
        fid = max_fid + 1
    conn.close()
    return fid


def update_file(fid, name, fpath, pid, desc, type_kw):
    conn = connect()
    cur = conn.cursor()
    sql = """insert into "file"(fid, fname, fpath, pid, description, upload_t, type)
         values (%s, %s, %s, %s, %s, %s, %s);"""
    cur.execute(sql, (fid, name, fpath, pid, desc, datetime.datetime.now(), type_kw))
    conn.commit()
    conn.close()
    return True