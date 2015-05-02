#-*- coding: utf-8-*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from bitirme.forms import LoginForm, RegisterForm
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import json


def index(request):
    title = "Thesis Repository"
    return render(request, 'index.html', locals())


@require_GET
def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    login_form = LoginForm()
    title = "Giriş Yap"
    return render(request, "login.html", locals())


@require_POST
def user_login_ajax(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": 0, "message": "Daha önceden giriş yapılmıştır."}), content_type="application/json")

    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        cleaned_data = login_form.cleaned_data
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({"status": 1, "message": "Başarı ile giriş yaptınız. Yönlendiriliyorsunuz."}), content_type="application/json")

    response = {"status": 0, "errors": login_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@require_GET
def create_account(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    title = "Create Your Account"
    register_form = RegisterForm()
    return render(request, "create_account.html", locals())


def create_account_ajax(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": 0, "message": "Daha önceden giriş yapılmıştır."}), content_type="application/json")

    register_form = RegisterForm(data=request.POST)
    if register_form.is_valid():
        register_form.save()
        return HttpResponse(json.dumps({"status": 1, "message": "Kayıt işlemi başarı ile gerçekleşti. Giriş sayfasına yönlendiriliyorsunuz."}), content_type="application/json")

    response = {"status": 0, "errors": register_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")