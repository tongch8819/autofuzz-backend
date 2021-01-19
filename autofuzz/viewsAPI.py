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
        # data is a dictionary
        req_data = json.loads(request.body.decode().replace("'", "\""))
        print(req_data)
        # print(data)
        # print(type(data))
        tplt = """insert into project(pid, pname, uid, description, upload_t)
         values (%s, %s, %s, %s, current_timestamp);"""
        data = (
            pid,
            req_data['name'],
            # '0B,',
            1,
            req_data['info'],
            # datetime.datetime.now(),
        )
        # print(insert_sql)
        cur.execute(tplt, data)
        conn.commit()
        conn.close()


        # response context
        ctx = {
            'pid': pid,
            'name': req_data['name'],
            'info': req_data['info'],
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
    # print(request.FILES)
    my_file = request.FILES.get('file')
    base_path = os.fspath(settings.BASE_DIR) 
    trgt_path = base_path + "/asset/tmp"
    with open(trgt_path + "/project.tar.gz", 'bw') as wrt:
        for chunk in my_file.chunks():
            wrt.write(chunk)


    ctx = {
        'status': 'OK',
    }

    return JsonResponse(ctx)


def upload_inputseed(request):
    my_file = request.FILES.get('file')
    base_path = os.fspath(settings.BASE_DIR) 
    trgt_path = base_path + "/asset/tmp"

    with open(trgt_path + "/input" + str(random.randint(1,100)) + ".txt", 'bw') as wrt:
        for chunk in my_file.chunks():
            wrt.write(chunk)

    ctx = {
        'status': 'OK',
    }
    return JsonResponse(ctx)


def compile(request):
    # bin fid
    fid = db_util.generate_fid()

    # parse
    src_fid = request.POST.get('fid')
    compiler_id = request.POST.get('type')
    project_id = request.POST.get('pid')

    src_name = "something"
    bin_name = "something"

    manage_path = os.fspath(settings.BASE_DIR) + '/asset/script/manage_pool.py'
    tplt = "python {} {} {} {} {} {}"
    cmd = tplt.format(
        manage_path,
        "compile",
        project_id,
        compiler_id,
        src_name,
        bin_name,
    )
    code = os.system(cmd)
    ctx = {
        'fid': fid,
        'status': 'OK' if code == 0 else "ERROR",
    }
    return JsonResponse(ctx)


def get_project_id(name):
    conn = db_util.connect()
    cur = conn.cursor()
    sql = """select pid from "project" where pname = '{}';""" .format(name)
    cur.execute(sql)
    return cur.fetchone()[0]

def get_kernel_id(name):
    conn = db_util.connect()
    cur = conn.cursor()
    sql = """select fid from "fuzzer" where fname = '{}';""" .format(name)
    cur.execute(sql)
    return cur.fetchone()[0]


def run(request):
    # project_id = request.POST.get('project_id')
    # bin_name = request.POST.get('bin_name')
    # kernel_id = request.POST.get('kernel_id')
    data_dict = json.loads(request.body.decode().replace("'", "\""))
    print(data_dict)

    project_id = get_project_id(data_dict['projectName'])
    kernel_id = get_kernel_id(data_dict['kernelType'])
    bin_name = 'demo'
    base_path = os.fspath(settings.BASE_DIR)
    manage_path = base_path + '/asset/script/manage_pool.py'

    # preprocess
    tplt_prep = "python {} {} {} {}"
    cmd_prep = tplt_prep.format(
        manage_path,
        'preprocess',
        'init',
        project_id
    )
    print(cmd_prep)
    os.system(cmd_prep)

    tmp_path = base_path + '/asset/tmp'
    trgt_path = base_path + '/asset/pool/' + str(project_id)
    os.system("mv " + tmp_path + "/* " + trgt_path + '/src/')
    os.system("tar xzvf " + trgt_path + "/src/project.tar.gz -C " + trgt_path + '/src')
    os.system("rm " + trgt_path + "/src/project.tar.gz")
    # cp all input file into input
    os.system("cp " + trgt_path + "/src/* " + trgt_path + '/input/')
    os.system("cp " + trgt_path + "/src/afl-demo/target.c " + trgt_path + '/src/')
    os.system("cp " + trgt_path + "/src/afl-demo/input/* " + trgt_path + '/input/')

    # compile
    src_name = "target.c"

    tplt_compile = "python {} {} {} {} {} {}"
    cmd_compile = tplt_compile.format(
        manage_path,
        "compile",
        project_id,
        kernel_id,
        src_name,
        bin_name,
    )
    print(cmd_compile)
    os.system(cmd_compile)

    # run
    tplt = "python {} {} {} {} {}"
    cmd = tplt.format(
        manage_path,
        "run",
        project_id,
        bin_name,
        kernel_id,
    )
    print(cmd)
    code = os.system(cmd)

    code = 0
    ctx = {
        'status': 'OK' if code == 0 else "ERROR"
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


def query_single_project_info(request, project_id):
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


def query_disk_snapshot(request):
    cmd = "df -h | head -n 4 | tail -n 1"
    fd = os.popen(cmd)
    rst = fd.read()
    tokens = rst.split()
    print(tokens)
    ctx = {
        "disk_used_percent": tokens[-2],
        "disk_used": tokens[2],
        "disk_total": tokens[1]
    }
    return JsonResponse(ctx)


def process_list():
    item_list = []
    for proc in psutil.process_iter():
        try:
            p_info = proc.as_dict(attrs=[
                'pid', 'name', 'username', 'cpu_percent', 'memory_full_info'])
        except:
            pass
        else:
            # p_info is a dictionary
            item_list.append(p_info)
    return item_list

def filter_process_list() -> (list, int):
    content = process_list()
    def filterUser(info: dict):
        if info['username'] == 'root':
            return False
        # if info['cpu_percent'] == 0.0:
            # return False
        if info['memory_full_info'] is None:
            return False
        return True

    filterContent = [x for x in content if filterUser(x)]
    return filterContent, len(content)


def query_process_list(request):
    # rd = os.popen('ps aux | head -n 10')
    # content = rd.read()
    filterContent, length_content = filter_process_list()
    ctx = {
        'user_process_list': filterContent,
        'system_total': length_content,
        'user_total': len(filterContent),
    }
    return JsonResponse(ctx)


import datetime
def fake_list(request):
    ctx = {
        'project-item-list': [],
    }
    ks = ['id', 'pid', 'title', 'subDescription', 'owner', 'percent', 'avatar', 'status', 'cover', 'logo']
    # ks = ['id', 'title', 'subDescription', 'owner', 'percent', 'status', 'cover']

    conn = db_util.connect()
    cur = conn.cursor()
    sql = """select "project".pid, "project".pname,  "project".description, "user".username, "project".upload_t from "project", "user" 
        where "project".uid = "user".uid;
        """
    cur.execute(sql)

    def compute_percent(start: datetime.datetime) -> int:
        now = datetime.datetime.now()
        interval = now - start
        total = datetime.timedelta(hours=5)
        percent = interval / total  # timedelta operation
        return int(eval("{:2}".format(percent*100)))


    for i, line in enumerate(cur.fetchall()):
        """
        ('base64', 'Unknown',  datetime.datetime(2021, 1, 19, 10, 22, 49, 789094), 'zhangsan')
        """
        obj = dict()
        # avatar_url = 'data:image/jpeg;base64,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'
        avatar_url = 'https://api.prodless.com/avatar.png?size=48'
        cover_url = 'https://gw.alipayobjects.com/zos/rmsportal/iZBVOIhGJiAnhplqjvZW.png'
        logo_url = avatar_url
        percent = compute_percent(line[-1])
        status = 'active' if percent >= 100 else 'exception'
        vals = ['fake-list-'+ str(i)] + list(line[:-1]) + [percent, avatar_url, status, cover_url, logo_url]
        # print(vals)
        for k, v in zip(ks, vals):
            obj[k] = v
        ctx['project-item-list'].append(obj)

    conn.close()
    return JsonResponse(ctx['project-item-list'], safe=False)


from PIL import Image
from django.http import HttpResponse
from django.conf import settings
def avatar(request):
    valid_image = os.fspath(settings.BASE_DIR / "static" / "img" / "bug.png")
    try:
        with open(valid_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response


def status_data(request):
    ctx = {
        'visitData': [],
        'visitData2': [],

        'salesData': [],
        'searchData': [],
        'salesTypeData': [],
        'salesTypeDataOnline': [],
        'salesTypeDataOffline': [],

        'offlineData': [],
        'offlineChartData': [],
    }
    # visit data
    for i in range(16):
        tmp = dict()
        tmp['x'] = '2021-01-{}'.format(i+8) 
        tmp['y'] = random.randint(20, 70)
        ctx['visitData'].append(tmp)
        ctx['visitData2'].append(tmp)
    
    # sales data
    month_end = [
        '2020-12-31 23:00:00',
        '2021-01-31 23:00:00',
        '2021-02-28 23:00:00',
        '2021-03-31 23:00:00',
        '2021-04-30 23:00:00',
        '2021-05-31 23:00:00',
        '2021-06-30 23:00:00',
        '2021-07-31 23:00:00',
        '2021-08-31 23:00:00',
        '2021-09-30 23:00:00',
        '2021-10-31 23:00:00',
        '2021-11-30 23:00:00',
        '2021-12-31 23:00:00',
    ]
    tplt = """select count(cid) from "crash" where trigger_t > '{}' and 
    trigger_t <= '{}';"""
    month = 1
    for left, right in zip(month_end[:-1], month_end[1:]):
        sql = tplt.format(left, right)
        cnt = db_util.select(sql)[0][0]
        ctx['salesData'].append({
            'x': str(month) + "月",
            "y": cnt,
        })
        month += 1

    # search data
    searchData_ks = ['index', 'keyword', 'count', 'range', 'status']
    filter_process_content, _ = filter_process_list()
    mem_total = psutil.virtual_memory().total
    for process in filter_process_content:
        tmp = dict()
        memory_precent = process['memory_full_info'][0] * 100/ mem_total
        vals = [process['pid'], process['name'], process['cpu_percent'], "{:.2f}".format(memory_precent), random.choice([0, 1])]
        for k, v in zip(searchData_ks, vals):
            tmp[k] = v
        ctx['searchData'].append(tmp)

    salesType_ks = ['AFL', 'MemLock', 'MOpt', 'Triforce', 'AFLPlusPlus']
    vals = [random.randint(10,50) for _ in range(len(salesType_ks))]
    for k, v in zip(salesType_ks, vals):
        ctx['salesTypeData'].append({"x":k, "y":v})
        ctx['salesTypeDataOnline'].append({"x":k, "y":v + random.randint(50, 100)})
    ctx['salesTypeDataOffline'] = ctx['salesTypeDataOnline']

    for i in range(15):
        tmp = dict()
        tmp['x'] = i + 1
        tmp['y1'] = random.randint(10, 50)
        tmp['y2'] = random.randint(50, 200)
        ctx['offlineChartData'].append(tmp)

    return JsonResponse(ctx)

def ranking_list_data(request):
    ctx = {
        'payload': [],
        'status': 'OK',
    }

    conn = db_util.connect()
    cur = conn.cursor()
    sql = """select tmp.fname, count(tmp.cid) from 
(select * from "crash", "fuzzer" where "crash".fuzzer_id = "fuzzer".fid) as tmp
group by tmp.fname
order by tmp.count desc;"""
    cur.execute(sql)
    i = 0
    for title, total in cur.fetchall():
        tmp = dict()
        tmp['title'] = title
        tmp['total'] = total
        tmp['i'] = i
        i += 1
        ctx['payload'].append(tmp)
    conn.close()
    return JsonResponse(ctx)

def query_project_info(request):
    ctx = dict()
    sql = """select count(pid) from "project";"""
    ctx['total'] = db_util.select(sql)[0][0]

    sql = """select count(pid) from "project" where upload_t > upload_t - interval '7 days';"""
    ctx['week'] = db_util.select(sql)[0][0]

    sql = """select count(pid) from "project" where upload_t > upload_t - interval '30 days';"""
    ctx['month'] = db_util.select(sql)[0][0]
    return JsonResponse(ctx)