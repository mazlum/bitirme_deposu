#-*- coding: utf-8-*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from bitirme.forms import LoginForm, RegisterForm, EditProfileForm, ThesisForm, SearchForm
from bitirme.models import Users, File, Image, Thesis
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
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
        return HttpResponse(json.dumps({"status": 0, "message": "Daha önceden giriş yapılmıştır."}),
                            content_type="application/json")

    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        cleaned_data = login_form.cleaned_data
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(json.dumps({"status": 1, "message": "Başarı ile giriş yaptınız. Yönlendiriliyorsunuz."}),
                                    content_type="application/json")

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


@require_POST
def create_account_ajax(request):
    if request.user.is_authenticated():
        return HttpResponse(json.dumps({"status": 0, "message": "Daha önceden giriş yapılmıştır."}),
                            content_type="application/json")

    register_form = RegisterForm(data=request.POST)
    if register_form.is_valid():
        register_form.save()
        return HttpResponse(json.dumps({"status": 1, "message": "Kayıt işlemi başarı ile gerçekleşti. "
                                                                "Giriş sayfasına yönlendiriliyorsunuz."}),
                            content_type="application/json")

    response = {"status": 0, "errors": register_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_GET
def about(request):
    title = "Hakkında"
    return render(request, "about.html", locals())


@require_GET
@login_required
def profile(request):
    title = "Profil"
    profile_form = EditProfileForm(instance=request.user)
    return render(request, "profile.html", locals())


@require_POST
@login_required
def profile_ajax(request):
    profile_form = EditProfileForm(data=request.POST, instance=request.user, files=request.FILES)
    if profile_form.is_valid():
        clean_data = profile_form.cleaned_data
        print clean_data
        profile_form.save()
        return HttpResponse(json.dumps({"status": 1, "message": "Güncelleme işlemi başarılı bir şekilde gerçekleşti."}),
                            content_type="application/json")
    response = {"status": 0, "errors": profile_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_GET
def user_profile(request, username):
    user = get_object_or_404(Users, username=username)
    title = user.username
    return render(request, "user_profile.html", locals())


@require_GET
@login_required
def thesis_create(request):
    title = "Tez Oluşturma"
    thesis_form = ThesisForm()
    return render(request, "thesis_create.html", locals())


@transaction.atomic
@login_required
@require_POST
def thesis_create_ajax(request):
    thesis_form = ThesisForm(data=request.POST, instance=request.user, files=request.FILES)
    if thesis_form.is_valid():
        sid = transaction.savepoint()
        try:
            clean_data = thesis_form.cleaned_data
            file_list = [File.objects.create(file=thesis_file)for thesis_file in clean_data.get('files')]
            image_list = [Image.objects.create(image=thesis_image) for thesis_image in clean_data.get('images')]
            thesis = Thesis(user=request.user, name=clean_data.get("name"), content=clean_data.get('content'))
            thesis.save()
            thesis.image.add(*image_list)
            thesis.file.add(*file_list)
        except Exception, e:
            transaction.savepoint_rollback(sid)
            if request.user.is_authenticated():
                return HttpResponse(json.dumps({"status": 0, "message": "Oluşturma sırasında bir hata oluştu. Lütfen "
                                                                        "daha sonra tekrar deneyin. Hata düzelmez ise, "
                                                                        "yöneticiye başvurun"}),
                                    content_type="application/json")
        else:
            transaction.savepoint_commit(sid)

        return HttpResponse(json.dumps({"status": 1, "message": "Oluşturma işlemi başarı ile gerçekleşti. Profil "
                                                                "sayfasına yönlendiriliyorsunuz."}),
                            content_type="application/json")
    response = {"status": 0, "errors": thesis_form.errors.as_json()}
    return HttpResponse(json.dumps(response), content_type="application/json")


@require_GET
def theses(request):
    title = "Tezler"
    page = request.GET.get("sayfa", 1)

    all_theses = Thesis.objects.all()
    theses_pages = Paginator(all_theses, 10, request=request)

    try:
        theses = theses_pages.page(page)
    except EmptyPage:
        return HttpResponseRedirect('/')
    except PageNotAnInteger:
        return HttpResponseRedirect('/')

    return render(request, 'theses.html', locals())


@require_GET
def thesis_show(request, slug):
    thesis = get_object_or_404(Thesis, slug=slug)
    title = thesis.name
    return render(request, 'thesis_show.html', locals())


def search(request):
    page = request.GET.get("sayfa", 1)
    title = "Arama"
    search_form = SearchForm(data=request.GET)
    if search_form.is_valid():
        clean_data = search_form.cleaned_data

        all_theses = Thesis.objects.filter(name__icontains=clean_data['q'])

        theses_pages = Paginator(all_theses, 10, request=request)

        try:
            theses = theses_pages.page(page)
        except EmptyPage:
            return HttpResponseRedirect('/')
        except PageNotAnInteger:
            return HttpResponseRedirect('/')

        title = clean_data['q']
    return render(request, "search.html", locals())
