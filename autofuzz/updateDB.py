import os, sys
sys.path.append(".")
import db_util
import datetime
# from django.conf import settings

def get_fuzzer_id(project_id):
    sql = """select fuzzer_id from "project" where pid = {};""".format(project_id)
    return db_util.select(sql)[0][0]

def update_crash_table():
    conn = db_util.connect()
    cur = conn.cursor()

    delete_sql = """delete from "crash";"""
    cur.execute(delete_sql)

    insert_sql = """insert into "crash"(cid, seed_name, project_id, fuzzer_id, trigger_t) values
     (%s, %s, %s, %s, %s);"""
    # work_dir = os.fspath(settings.BASE_DIR) + '/asset/pool'
    work_dir = '/home/chengtong/auto-fuzz/fuzzing_platform/asset/pool'
    cid = 1

    for name in os.listdir(work_dir):
        pid = eval(name)
        crash_dir = work_dir + '/' + name + '/output/crashes'
        for seed_name in os.listdir(crash_dir):
            if seed_name == "README.txt":
                continue
            data = (cid, seed_name, pid, get_fuzzer_id(pid), datetime.datetime.now()-datetime.timedelta(hours=1)) 
            cur.execute(insert_sql, data)
            print(insert_sql, data)
            cid += 1
    conn.commit()
    conn.close()

def main():
    update_crash_table()

if __name__ == "__main__":
    main()