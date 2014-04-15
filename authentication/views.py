# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.formsets import formset_factory
import time
import json
from django.core.mail import mail_admins
from django.core.exceptions import ValidationError


class authorizationForm(forms.Form):
    username = forms.CharField(label=u'Логин',widget=forms.TextInput(attrs ={'size': 30, 'title': 'Логин', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести логин'}))
    password = forms.CharField(label=u'Пароль',widget=forms.PasswordInput(attrs ={'size': 30, 'title': 'Пароль', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести пароль'}))

class registrationForm(forms.Form):
    username = forms.CharField(label=u'Логин',widget=forms.TextInput(attrs ={'size': 30, 'title': 'Логин', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести логин'}))
    password = forms.CharField(label=u'Пароль',widget=forms.PasswordInput(attrs ={'size': 30, 'title': 'Пароль', 'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'Ввести пароль'}))
    email = forms.EmailField(label=u'email',widget=forms.TextInput(attrs ={'size': 30, 'title': 'email', 'class': 'form-control', 'id': 'inputEmail', 'placeholder': 'Ввести email'}))

class userControlForm(forms.Form):
    username = forms.CharField(label=u'Логин', widget=forms.TextInput(attrs ={'size': 20, 'title': 'Логин', 'class': 'form-control', 'id': 'inputLogin', 'placeholder': 'Ввести логин'}))
    password = forms.CharField(required=False, label=u'Пароль',widget=forms.PasswordInput(attrs ={'size': 20, 'title': 'Пароль', 'class': 'form-control', 'id': 'inputPassword', 'placeholder': 'Ввести пароль'}))
    email = forms.EmailField(label=u'email', widget=forms.TextInput(attrs ={'size': 20, 'title': 'email', 'class': 'form-control', 'id': 'inputEmail', 'placeholder': 'Ввести email'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs ={'title': 'superuser', 'class': 'form-control', 'id': 'checkboxSupeuser', 'placeholder': 'Суперпользователь'}))
    id =  forms.CharField(label=u'Логин', widget=forms.HiddenInput(attrs ={'class': 'userId', 'id': 'userId'}))

    

def username_check(username):
    if User.objects.filter(username=username).count():
        return True
    else:
        return False


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
                        #print "You provided a correct username and password!"
                        login(request,user)
                        print "---------------------Авторизован---------------------------"
                    else:
                        print "Your account has been disabled!"
                        print "---------------------Аккаунт отключен---------------------------"
                else:
                    print "Your username and password were incorrect."
                    print "---------------------Логин или пароль неккоректны---------------------------"
                 # Redirect after POST
        else:
            form = authorizationForm() # An unbound form
        return render(request, 'authentication/test1.html', {'form': form,})
    else:
        return HttpResponseRedirect('/')

def registration(request):
    if request.user.is_anonymous():
        print "---------------------Не авторизован---------------------------"
        return HttpResponseRedirect('/authentication/')
    else:

        if request.method == 'POST': # If the form has been submitted...
            form = registrationForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                if username_check(username):
                    print "-------------Пользователь с такми именем уже существует---------------"
                    form = registrationForm() # An unbound form
                    return render(request, 'authentication/registration.html', {'form': form,})
                else:
                    return username  
                    user = User.objects.create_user(username, email, password)
                    user.save()              
                    print "---------------------Пользователь создан---------------------------"
                    return render(request, 'authentication/congratulationRegistration.html')
                    time.sleep( 5 )
                    return HttpResponseRedirect('/')
                    print "!!!!!!!!!!!!!!!!!!!!!!!5!!!!!!!!!!!!!!!!!!!!!!"
        else:
            form = registrationForm() # An unbound form
            return render(request, 'authentication/registration.html', {'form': form,})

def userControl(request):
    if request.method == 'POST': # If the form has been submitted...
        
        
        form = userControlForm(request.POST) # A form bound to the POST data
#        print request.POST
        #form = formset(request.POST)
#        for i in request:
#            print i
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_superuser = form.cleaned_data['is_superuser']
            email = form.cleaned_data['email']
            user_id = form.cleaned_data['id']
            print "Всё прошло нормально"
            return render(request, 'authentication/usercontrol.html', {'userControlList': formset,})
        else:
            print "0"
    else:
        userlist = User.objects.all()
        userControlList = userControlForm
        ArticleFormSet = formset_factory(userControlForm,extra=0)
        data = []
        i = 0
        print userlist[0]
        for user in userlist:
            userdata = {}
            userdata['username'] = user.username
            userdata['email'] = user.email
            userdata['is_superuser']=user.is_superuser
            userdata['id']=user.id
            data.append(userdata)
            i+=1

        formset = ArticleFormSet(initial=data)

        return render(request, 'authentication/usercontrol.html', {'userControlList': formset,})