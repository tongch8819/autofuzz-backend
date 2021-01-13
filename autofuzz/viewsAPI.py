from django.shortcuts import render
from django.template.loader import get_template

from django.http import JsonResponse
import json


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

# to do
def create_project(request):
    ctx = {
        'pid' : 100,
        'info': 'something',
        'name': 'something',
    }
    return JsonResponse(ctx)

def upload_program(request):
    # request.POST.
    ctx = {
        'fid': 10005,
        'status': 'OK',
    }
    return JsonResponse(ctx)

def upload_inputseed(request):
    ctx = {
        'fid': 20005,
        'status': 'OK',
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

from . import views
def status(request):
    ctx = views.buildFuzzerStatCtx()
    return JsonResponse(ctx)