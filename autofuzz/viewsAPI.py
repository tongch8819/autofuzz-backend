import datetime
from . import views
from . import db_util
from django.shortcuts import render
from django.template.loader import get_template

from django.http import JsonResponse
import os
import sys
import random
import json
from django.conf import settings
import psutil


def memoryUsage(request):
    return JsonResponse(
        {
            'virtual': '1000',
            'resident': '500',
        }
    )


def cpuUsage(request):
    return JsonResponse({
        'cpu-time': '08:32',
        'cpu-percent': '1.46%',
    })


def diskUsage(request):
    return JsonResponse({
        'projects': [{
            'id': 1,
            'name': 'uniq.tar.gz',
            'size': '346M',
        },
            {
            'id': 2,
            'name': 'base64.tar.gz',
            'size': '100M',
        },
            {
            'id': 3,
            'name': 'asn1c.tar.gz',
            'size': '524M',
        },
        ]
    })


def create_project(request):
    try:
        # generate pid
        conn = db_util.connect()
        cur = conn.cursor()
        sql = 'select max("pid") from "project";'
        cur.execute(sql)
        pid = cur.fetchone()[0]
        if pid is None:
            pid = 1
        else:
            pid += 1

        # update database
        # tplt = "insert into project values ({0}, {1}, {2}, {3}, {4}, {5});"
        tplt = """insert into project(pid, pname, uid, description) values (%s, %s, %s, %s);"""
        data = (
            pid,
            request.POST.get('name'),
            # '0B,',
            1,
            request.POST.get('info'),
            # datetime.datetime.now(),
        )
        # print(insert_sql)
        cur.execute(tplt, data)
        conn.commit()
        conn.close()

        # response context
        ctx = {
            'pid': pid,
            'name': request.POST.get('name'),
            'info': request.POST.get('info'),
            'status': 'OK'
        }
    except:
        # response context
        ctx = {
            'pid': pid,
            'name': request.POST.get('name'),
            'info': request.POST.get('info'),
            'status': 'ERROR'
        }
    return JsonResponse(ctx)


def upload_program(request):
    try: 
        # generate fid
        conn = db_util.connect()
        cur = conn.cursor()
        sql = """select max("fid") from "file";"""
        cur.execute(sql)
        max_fid = cur.fetchone()[0]
        if max_fid is None:
            fid = 1
        else:
            fid = max_fid + 1

        # parse POST form
        name = request.POST.get('name')
        pid = request.POST.get('pid')
        fpath = os.fspath(settings.BASE_DIR) + '/asset/pool/' + \
            str(pid) + '/src/' + name  # str
        desc = request.POST.get('info')
        type_kw = request.POST.get('type')

        # write file into fpath

        # update database
        sql = """insert into "file"(fid, fname, fpath, pid, description, upload_t, type)
         values (%s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (fid, name, fpath, pid, desc,
                          datetime.datetime.now(), type_kw))
        conn.commit()
        conn.close()

        # json response
        ctx = {
            'fid': fid,
            'status': 'OK',
        }
    except:
        # json response
        ctx = {
            'fid': fid,
            'status': 'ERROR',
        }

    return JsonResponse(ctx)


def upload_inputseed(request):
    try: 
        # generate fid
        conn = db_util.connect()
        cur = conn.cursor()
        sql = """select max("fid") from "file";"""
        cur.execute(sql)
        max_fid = cur.fetchone()[0]
        if max_fid is None:
            fid = 1
        else:
            fid = max_fid + 1

        # parse POST form
        name = request.POST.get('name')
        pid = request.POST.get('pid')
        fpath = os.fspath(settings.BASE_DIR) + '/asset/pool/' + \
            str(pid) + '/input/' + name  # str
        desc = request.POST.get('info')
        # type_kw = request.POST.get('type')
        type_kw = 'inputseed'

        # write file into fpath

        # update database
        sql = """insert into "file"(fid, fname, fpath, pid, description, upload_t, type)
         values (%s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(sql, (fid, name, fpath, pid, desc,
                          datetime.datetime.now(), type_kw))
        conn.commit()
        conn.close()

        # json response
        ctx = {
            'fid': fid,
            'status': 'OK',
        }
    except:
        # json response
        ctx = {
            'fid': fid,
            'status': 'ERROR',
        }
    return JsonResponse(ctx)


def compile(request):
    ctx = {
        'fid': 30005,
        'status': 'OK',
    }
    return JsonResponse(ctx)


def run(request):
    ctx = {
        'status': 'OK'
    }
    return JsonResponse(ctx)


def status(request):
    ctx = views.buildFuzzerStatCtx()
    return JsonResponse(ctx)


def query_project_list(request):
    conn = db_util.connect()
    sql = """select * from "project";"""
    cur = conn.cursor()
    cur.execute(sql)
    # container = cur.fetchall()
    container = []
    keys = ['pid', 'name', 'size', 'uid', 'info', 'upload_t']
    for item in cur.fetchall():
        tmp = {k: v for k, v in zip(keys, item)}
        container.append(tmp)
    ctx = {
        'project_list': container
    }
    return JsonResponse(ctx)


def query_project_info(request, project_id):
    conn = db_util.connect()
    sql = """select * from "project";"""
    cur = conn.cursor()
    cur.execute(sql)
    # container = cur.fetchall()
    keys = ['pid', 'name', 'size', 'uid', 'info', 'upload_t']
    for item in cur.fetchall():
        # print(type(item[0]))
        if item[0] == project_id:
            tmp = {k: v for k, v in zip(keys, item)}
            break
    ctx = {
        'project_id': project_id,
        'project_info': tmp['info'],
    }
    return JsonResponse(ctx)


def query_file_list(request, project_id):
    base_path = settings.BASE_DIR
    # a = os.fspath(base_path)
    # print(a)
    # print(type(a))
    # print(base_path)
    # print(type(base_path))
    container = [name for name in os.walk(
        base_path / 'asset' / 'pool' / str(project_id))]
    ctx = {
        'walk of directory': container,
    }
    return JsonResponse(ctx)


def query_cpu_snapshot(request):
    cpu_times = psutil.cpu_times()
    ctx = {
        'cpu_times_user': cpu_times.user,
        'cpu_times_nice': cpu_times.nice,
        'cpu_times_system': cpu_times.system,
        'cpu_times_idle': cpu_times.idle,
        'cpu_times_iowait': cpu_times.iowait,
        'cpu_times_irq': cpu_times.irq,
        'cpu_times_softirq': cpu_times.softirq,
        'cpu_times_steal': cpu_times.steal,
        'cpu_times_guest': cpu_times.guest,
        'cpu_count': psutil.cpu_count(),
        'cpu_percent': psutil.cpu_percent(),
    }
    return JsonResponse(ctx)


def query_memory_snapshot(request):
    mem = psutil.virtual_memory()
    ctx = {
        'memory_total': mem.total,
        'memory_used': mem.used,
        'memory_free': mem.free,
        'memory_used_percent': mem.used / mem.total,
        'memory_free_percent': mem.free / mem.total,
    }
    return JsonResponse(ctx)


def query_cpu_timeseries(request):
    ctx = {
        'cpu_ts': [random.random() for _ in range(100)],  # fake
        'cpu_percent_now': psutil.cpu_percent(),
    }
    return JsonResponse(ctx)


def query_memory_timeseries(request):
    mem = psutil.virtual_memory()
    ctx = {
        'memory_ts': [random.random() for _ in range(100)],
        'memory_used_percent_now': mem.used / mem.total,
    }
    return JsonResponse(ctx)


def process_list():
    item_list = []
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=['pid', 'name'])
        except:
            pass
        else:
            # p_info is a dictionary
            item_list.append(p_info)
    return item_list


def query_process_list(request):
    # rd = os.popen('ps aux | head -n 10')
    # content = rd.read()
    content = process_list()
    ctx = {
        'process_list': content,
    }
    return JsonResponse(ctx)
