# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from django import forms




def index(request):
    if request.user.is_anonymous():
        print "---------------------Не авторизован---------------------------"
        return HttpResponseRedirect('/authentication/')
    else:
        #render(request, 'authentication/test1.html')
        print "---------------------Авторизован---------------------------"
        template = loader.get_template('main/index.html')
        page = RequestContext(request)
        return HttpResponse(template.render(page))