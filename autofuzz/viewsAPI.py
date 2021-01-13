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