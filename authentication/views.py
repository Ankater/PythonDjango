# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect


class authorizationForm(forms.Form):
    username = forms.CharField(label=u'Логин',widget=forms.TextInput(attrs ={'size': 30, 'title': 'Логин', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести логин'}))
    password = forms.CharField(label=u'Пароль',widget=forms.PasswordInput(attrs ={'size': 30, 'title': 'Пароль', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести пароль'}))



def authorization(request):
    if request.user.is_anonymous():
        if request.method == 'POST': # If the form has been submitted...
            form = authorizationForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        print "You provided a correct username and password!"
                        login(request,user)
                        return HttpResponseRedirect('/')
                    else:
                        print "Your account has been disabled!"
                        return HttpResponseRedirect('/2')
                else:
                    print "Your username and password were incorrect."
                    return HttpResponseRedirect('/0 ')
                 # Redirect after POST
        else:
            form = authorizationForm() # An unbound form
        return render(request, 'authentication/test1.html', {'form': form,})
    else:
        return HttpResponseRedirect('/')