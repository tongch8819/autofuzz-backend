from . import views
from django.conf.urls import url



urlpatterns = [
    url(r'^folder/(?P<url>.+)/$', views.show_folder),
    url(r'^$', views.index),
]