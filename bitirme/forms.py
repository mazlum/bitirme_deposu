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


class ProfileAdminForm(forms.ModelForm):
    def save(self, commit=True):

        user = super(ProfileAdminForm, self).save(commit=False)

        if(len(user.password) != 77):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email