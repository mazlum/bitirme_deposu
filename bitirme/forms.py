#-*- coding: utf-8 -*-
from django.contrib.auth.forms import *
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.utils.encoding import force_bytes


class LoginForm(AuthenticationForm):
    captcha = NoReCaptchaField(error_messages={'required': 'Captcha zorunludur', 'invalid': 'Geçersiz Captcha'},
                               gtag_attrs={'data-theme': 'dark'})
    username = forms.CharField(error_messages={'required': 'Kullanıcı adı zorunludur', 'invalid': 'Geçersiz kullanıcı adı'},
                               label='Kullanıcı Adı', widget=forms.TextInput(attrs={'class': 'form-control input-lg'}))
    password = forms.CharField(error_messages={'required': 'Şifre zorunludur', 'invalid': 'Geçersiz şifre'},
                               label='Şifre', widget=forms.PasswordInput(attrs={'class': 'form-control input-lg'}))

    error_messages = {
        'invalid_login': force_bytes("Geçersiz kullanıcı adı veya şifre"),
        'inactive': force_bytes("Bu hesap yönetici tarafından askıya alınmıştır. Lütfen yöneticiye başvurunuz."),
    }