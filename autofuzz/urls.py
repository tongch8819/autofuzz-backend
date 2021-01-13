from django.conf.urls import url
from django.urls import path
from . import views, viewsAPI

urlpatterns = [
    url('test', views.test, name='test'),

    # match None or index
    url(r'^[index]*$', views.index, name='index'),
    url(r'^help$', views.help, name='help'),
    url('create-project', views.create_project, name='create_project'),
    url('my-project', views.my_project, name='my_project'),
    url('settings', views.settings, name='settings'),

    url('dashboard', views.dashboard, name='dashboard'),
    # url(r'^contact$', views.contact, name='contact'),
    url(r'^uploadCompress$', views.uploadCompress, name='uploadCompress'),
    url(r'^uploadGitURL$', views.uploadGitURL, name='uploadGitURL'),
    url(r'^uploadInputSeeds$', views.uploadInputSeeds, name='uploadInputSeeds'),
    
    url(r'^returnUploadResult/$', views.getFile, name='getFile'),
    
    url(r'^compile/$', views.compile, name='compile'),
    url(r'^runtime/$', views.runtime, name='runtime'),
    url(r'^status/$', views.status, name='status'),
    url(r'^asktime/$', views.asktime, name='asktime'),
    url(r'^download/$', views.download, name='download'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^stop/$', views.stop, name='stop'),

    url(r'^report/$', views.report, name='report'),
    url('PDFReport', views.PDFReport, name='PDFReport'),

    url('hello', views.sayHello, name="sayHello"),

    # download crash input seed
    path('download/project/<int:project_id>/crash/<str:crash_id>', views.downloadCrashSeed, name='downloadCrashSeed'),

    # json api
    url('api/memory', viewsAPI.memoryUsage, name="memoryUsage"),
    url('api/cpu', viewsAPI.cpuUsage, name="cpuUsage"),
    url('api/disk', viewsAPI.diskUsage, name="diskUsage"),

    # -------
    # new api
    url('api/create/project', viewsAPI.create_project, name='create_project'),
    url('api/upload/program', viewsAPI.upload_program, name='upload_program'),
    url('api/upload/inputseed', viewsAPI.upload_inputseed, name='upload_inputseed'),
    url('api/compile', viewsAPI.compile, name='compile'),
    url('api/run', viewsAPI.run, name='run'),
    url('api/status', viewsAPI.status, name='status'),
]