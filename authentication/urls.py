from django.conf.urls import patterns, url
from authentication import views


urlpatterns = patterns('',
    url(r'^$', views.contact, name='index')
)
