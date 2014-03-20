# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect

def index(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect('/authentication/')
		#print "asfdsfdsfggfdyuugh"
	else:
		return HttpResponseRedirect('authentication/1111')
		print "great"