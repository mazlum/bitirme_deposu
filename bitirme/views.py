#-*- coding: utf-8-*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from bitirme.forms import LoginForm
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json


def index(request):
    return render(request, 'index.html', locals())


@require_POST
def user_login(request):
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

    print login_form.errors
    response = {"status": 0, "errors": login_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')