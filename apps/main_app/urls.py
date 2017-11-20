from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^/dashboard$', views.dashboard),
    url(r'^/add$', views.add),
    url(r'^/addtofavorites/(?P<id>\d+$)', views.addtofavorites),
    url(r'^/removefromfavorites/(?P<id>\d+$)', views.removefromfavorites),
    url(r'^/show/(?P<id>\d+$)', views.show),
]
