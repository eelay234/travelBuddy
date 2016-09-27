from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.create),
    url(r'^show_trip/(\d+)/$', views.show_trip),
    url(r'^join/(\d+)/$', views.join),
    url(r'^create_plan$', views.create_plan),
    url(r'^show_dashboard$', views.show_dashboard),
    url(r'^registration$', views.registration),
    url(r'^logoff$', views.logoff),
    url(r'^login$', views.login),
    url(r'^$', views.index)
]
