import pdfkit
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect

import os, re
import time
from datetime import datetime, timedelta
from django.conf import settings


def test(request):
    return render(request, 'autofuzz/test.html')

# Create your views here.


def index(request):
    template = get_template('autofuzz/index.html')
    return HttpResponse(template.render(dict(), request))
    # return render(request, 'html/index.html')


def help(request):
    return render(request, 'autofuzz/index.html')


def create_project(request):
    return render(request, 'autofuzz/create-project.html')


def my_project(request):
    return render(request, 'autofuzz/index.html')




def dashboard(request):
    return render(request, 'autofuzz/dashboard.html')


def uploadCompress(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

    # template = loader.get_template('upload/index.html')
    # return HttpResponse(template.render(context, request))

    # if request.method == 'POST':
    #     # form = nameForm(request.POST)
    #     # context = dict()
    #     # if form.is_valid():
    #     #     context['a'] = form.cleand_data['data']
    #     #     context['b'] = form.cleand_data['username']
    #     #     context['c'] = form.cleand_data['email']
    #     # else:
    #     #     context['a'] = 'Ooops'
    #     context = dict()
    #     context['a'] = request.POST.get['data']
    #     context['b'] = request.POST.get['username']
    #     context['c'] = request.POST.get['email']
    #     return render(request, 'upload/uploadCompress.html', context)
    # else:
    #     return render(request, 'upload/uploadCompress.html')
    return render(request, 'autofuzz/uploadCompress.html')


def uploadGitURL(request):
    return render(request, 'autofuzz/uploadGitURL.html')


def uploadInputSeeds(request):
    return render(request, 'autofuzz/uploadInputSeeds.html')


def getFile(request):
    kw_list = ['file_type', 'git_url']
    value = None
    for keyword in kw_list:
        value = request.POST.get(keyword)
        if value is not None:
            break
    if value is None:
        return render(request, "autofuzz/returnUploadResult.html")

    context = dict()
    base_path = os.fspath(settings.BASE_DIR) + "/asset"
    if keyword == 'file_type':
        myfile = request.FILES.get('input_file')
        if value == "input_seed":
            path = base_path + "/target/input.txt"
        elif value == "project":
            path = base_path + "/project.tar.gz"
        try:
            with open(path, 'bw') as wrt_fd:
                for chunk in myfile.chunks():
                    wrt_fd.write(chunk)
            if path == base_path + "/project.tar.gz":
                os.system("cd " + base_path + "; tar xzvf project.tar.gz")
            context['status'] = "succeed"
        except IOError as e:
            print(e)
            context['status'] = "failed"
    else:
        os.system('git clone ' + value)
        context['status'] = "succeed"
    return render(request, "autofuzz/returnUploadResult.html", context)


def compile(request):
    return render(request, "autofuzz/compile.html")


def runtime(request):
    if request.GET.get("compile") == "插桩编译":
        if request.GET.get("kernel_type") == "afl":
            os.system("bash asset/compile.sh afl")
        elif request.GET.get("kernel_type") == "memlock":
            os.system("bash asset/compile.sh memlock")
        else:
            os.system("bash asset/compile.sh")
    return render(request, 'autofuzz/runtime.html')


def status(request):
    context = dict()
    if request.GET.get("run") == "运行模糊测试任务":
        context['run'] = "running"
        if request.GET.get("kernel_type") == "afl":
            os.system("bash asset/run.sh afl")
        elif request.GET.get("kernel_type") == "memlock-heap":
            os.system("bash asset/run.sh memlock-heap")
        elif request.GET.get("kernel_type") == "memlock-stack":
            os.system("bash asset/run.sh memlock-stack")
        else:
            os.system("bash asset/run.sh")
    elif request.GET.get("clean") == "清理历史记录":
        context['run'] = "历史记录清除完毕"
        os.system("rm -rf asset/target/output")
    else:
        context['run'] = "debug"
    return render(request, 'autofuzz/status.html', context)


def asktime(request):
    ans = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(ans)
    return HttpResponse(ans)


def download(request):
    return render(request, "autofuzz/report.csv")





def panel(request):
    base_path = os.fspath(settings.BASE_DIR)
    with open(base_path + '/asset/target/output/fuzzer_stats', 'r') as rd:
        content = rd.readlines()

    context = dict()
    for line in content:
        k, v = line.replace(' ', '').strip().split(':')
        context[k] = v
    # context['asc_start_time'] = time.asctime(time.localtime(int(context['start_time'])))
    # context['asc_last_update'] = time.asctime(time.localtime(int(context['last_update'])))

    def _time_format(unix_time):
        datetime_obj = datetime.fromtimestamp(unix_time) + timedelta(hours=8)
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    context['asc_start_time'] = _time_format(int(context['start_time']))
    context['asc_last_update'] = _time_format(int(context['last_update']))

    context['panel_update_time'] = _time_format(time.time())

    def generateReport(ctx):
        container = []
        line_list = [
            ('开始时间', 'asc_start_time', '模糊测试任务启动的时刻'),
            ('上次更新时间', 'asc_last_update', '模糊测试上次更新种子的时刻'),
            ('循环轮次', 'cycles_done', '循环执行程序的次数'),
            ('总执行次数', 'execs_done', '执行程序的总次数'),
            ('每秒执行次数', 'execs_per_sec', '反映模糊测试进程的执行效率'),
            ('总路径数', 'paths_total', '模糊测试执行过程中覆盖到的总路径条数'),
            ('崩溃数', 'unique_crashes', '触发不同崩溃的次数'),
            ('挂起次数', 'unique_hangs', '程序运行过程中出现异常而挂起的次数'),
        ]
        for a, key, c in line_list:
            line = a + "," + ctx[key] + "," + c + "\n"
            container.append(line)
        return container

    content = generateReport(context)
    with open(base_path + "/autofuzz/templates/autofuzz/report.csv", "w") as wrt_fd:
        wrt_fd.writelines(content)

    return render(request, "autofuzz/panel.html", context)


def stop(request):
    base_path = os.fspath(settings.BASE_DIR) + "/asset"
    with open(base_path + '/target/output/fuzzer_stats', 'r') as rd:
        content = rd.readlines()
    _, pid = content[2].replace(' ', '').strip().split(':')
    # pid is str
    os.system("kill -KILL " + pid)
    context = dict()
    context['run'] = 'stop'
    return render(request, 'autofuzz/stop.html', context)












"""
Report Views
"""
def buildFuzzerStatCtx(project_id: int):
    base_path = os.fspath(settings.BASE_DIR) + "/asset"
    work_dir = base_path + '/pool/' + str(project_id) + '/output'

    # stat does not exist
    if not os.path.isfile(work_dir + '/fuzzer_stats'):
        return dict()

    with open(work_dir + '/fuzzer_stats', 'r') as rd:
        content = rd.readlines()
    context = dict()
    for line in content:
        k, v = line.replace(' ', '').strip().split(':')
        context[k] = v

    def _time_format(unix_time):
        datetime_obj = datetime.fromtimestamp(unix_time)
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    context['asc_start_time'] = _time_format(int(context['start_time']))
    context['asc_last_update'] = _time_format(int(context['last_update']))
    context['panel_update_time'] = _time_format(time.time())

    context['crash_item_list'] = []
    # construct crash information
    signal_dict = {
        1: 'SIGHUP',
        2: 'SIGINT',
        3: 'SIGQUIT',
        4: 'SIGKILL',
        5: 'SIGTRAP',
        6: 'SIGABRT',
        7: 'SIGBUS',
        8: 'SIGFPE',
        9: 'SIGKILL',
        10: 'SIGUSR1',
        11: 'SIGSEGV'
    }

    for name in os.listdir(work_dir + '/crashes'):
        if name == 'README.txt':
            continue
        tmp = dict()
        tokens = name.strip().split(',')
        print(tokens)
        for token in tokens:
            k, v = token.split(':')
            if k == 'sig':
                v = signal_dict[int(v)] if int(v) in range(1,12) else 'Unknown'
            tmp[k] = v
        context['crash_item_list'].append(tmp)
    return context

from . import db_util
def report(request, project_id):
    # fetch template from global directory
    sql = """select pname, size, description, upload_t from "project" where pid = {};""".format(project_id)
    rst = db_util.select(sql)[0]
    template = get_template('pdf/report.html')
    # print(type(rst[-1]))
    # print(rst[2])
    context = {
        'version': 'v1.0',
        'upload_t': rst[-1].strftime('%Y-%m-%d %H:%M'),
        # 'timestamp': time.asctime(time.localtime(time.time())),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),

        'project_name': rst[0],
        'size': rst[1],
        'description': rst[2],
        # 'md5': '09f1ee0e38387aa8ee813275b7f336b6',
        # 'sha1': 'ac4aa08760f47e3c5dea91b9a4d3aecbbeed5cfd',
        # 'sha256': 'f12a5eddc1caf40453b2b2d1d403a9a928c12fa8bd45bf26489c2cad2c172dbc',
    }

    context.update(buildFuzzerStatCtx(project_id))
    return HttpResponse(template.render(context))


def PDFReport(request, project_id):
    # options = {
        # 'page-size': 'Letter',
        # 'quiet': '',
        # 'no-collate': '',
        # 'margin-top': '0.50in',
        # 'margin-right': '0.50in',
        # 'margin-bottom': '0.50in',
        # 'margin-left': '0.50in',
        # 'encoding': 'UTF-8',
                    # 'custom-header': [
                        # ('Accept-Encoding', 'gzip'),
                    # ],
        # 'no-outline': None,
        # 'enable-local-file-access': True,
    # }
    url = '127.0.0.1:8002/autofuzz/report/' + str(project_id)
    # base_path = os.fspath(settings.BASE_DIR) + "/asset"
    output_path = os.fspath(settings.BASE_DIR) + '/asset/report/tmp.pdf'
    cmd = 'wkhtmltopdf ' + url + ' ' + output_path
    os.system(cmd)
    with open(output_path, 'rb') as rd:
        pdf_data = rd.read()
    return HttpResponse(pdf_data, content_type='application/pdf')


def sayHello(request):
    return render(request, 'autofuzz/sayHello.html')


def downloadCrashSeed(request, project_id, crash_id: str):
    base_dir = os.fspath(settings.BASE_DIR) + '/asset/pool/' + str(project_id) + '/output/crashes'
    if not os.path.isdir(base_dir):
        return render(request, 'autofuzz/404.html')

    regex = re.compile(crash_id)
    trgt_name = None
    for name in os.listdir(base_dir):
        if regex.search(name) is not None:
            trgt_name = name
            break
    if trgt_name is None:
        return render(request, 'autofuzz/404.html')
    with open(base_dir + '/' + name, 'r') as rd:
        content = rd.readlines()
    return HttpResponse(content, content_type='text/plain')


import random
def randomAvatar(request, name):
    work_dir = os.fspath(settings.BASE_DIR) + "/static/avatar"
    total = 50
    name = "{}.png".format(random.choice(list(range(1, total+1))))
    with open(work_dir + '/' + name, 'br') as rd:
        content = rd.read()
    return HttpResponse(content, content_type='img/png')


