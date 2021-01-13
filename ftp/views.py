from django.shortcuts import render
import os
from ftp.models import PathItem, FileItem

# Create your views here.


def index(request):
    current = '/home/chengtong/auto-fuzz/fuzzing_platform/asset/report'
    context_dic = {}
    context_dic['current'] = current
    ps = os.listdir(current)
    path_lst, file_lst = [], []
    for n in ps:
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, current)
            path_lst.append(p)
        else:
            f = FileItem(n, current)
            file_lst.append(f)
 
    context_dic['path'] = path_lst
    context_dic['file'] = file_lst
    return render(request, 'ftp/index.html', context_dic)
 
def show_folder(request, url):
    current = url
    context_dic = {}
    context_dic['current'] = current
    ps = os.listdir(current)
    path = []
    file = []
    for n in ps:
        v = os.path.join(current, n)
        if os.path.isdir(v):
            p = PathItem(n, current)
            path.append(p)
        else:
            f = FileItem(n, current)
            file.append(f)
 
    #context_dic['parent'] = os.path.pardir(url)
    context_dic['path'] = path
    context_dic['file'] = file

