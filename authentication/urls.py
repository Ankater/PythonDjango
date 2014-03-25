from django.conf.urls import patterns, url
from authentication import views


urlpatterns = patterns('',
    url(r'^$', views.authorization, name='index')
    url(r'^registration$', views.registration, name='index')
)
