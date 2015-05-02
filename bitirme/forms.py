# -*- coding: utf-8 -*-
from django.contrib.auth.forms import forms, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.utils.encoding import force_bytes
from models import Users, GRADE, SEX

ERROR_MESSAGES = {
    'invalid': 'Bu alan için geçersiz değer girdiniz',
    'required': 'Bu alan zorunludur',
}


class LoginForm(AuthenticationForm):
    captcha = NoReCaptchaField(error_messages={'required': 'Captcha zorunludur', 'invalid': 'Geçersiz Captcha'},
                               gtag_attrs={'data-theme': 'dark'})
    username = forms.CharField(
        error_messages={'required': 'Kullanıcı adı zorunludur', 'invalid': 'Geçersiz kullanıcı adı'},
        label='Kullanıcı Adı', widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'placeHolder': 'Kullanıcı adı'}))
    password = forms.CharField(error_messages={'required': 'Şifre zorunludur', 'invalid': 'Geçersiz şifre'},
                               label='Şifre', widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeHolder': 'Şifre'}))

    error_messages = {
        'invalid_login': force_bytes("Geçersiz kullanıcı adı veya şifre"),
        'inactive': force_bytes("Bu hesap yönetici tarafından askıya alınmıştır. Lütfen yöneticiye başvurunuz."),
    }


class ProfileAdminForm(forms.ModelForm):
    def save(self, commit=True):

        user = super(ProfileAdminForm, self).save(commit=False)

        if 77 != len(user.password):
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


class RegisterForm(UserCreationForm):
    captcha = NoReCaptchaField(error_messages={'required': 'Captcha zorunludur', 'invalid': 'Geçersiz Captcha'}, gtag_attrs={'data-theme': 'dark'})
    password1 = forms.CharField(label="Şifre", error_messages=ERROR_MESSAGES,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeHolder': 'Şifre'}))
    password2 = forms.CharField(label="Şifre Tekrar", error_messages=ERROR_MESSAGES,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeHolder': 'Şifre tekrar'}))

    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'university', 'department', 'grade', 'city',
                  'sex']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Kullanıcı adı'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeHolder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'İsim'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Soyisim'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Üniversite'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Bölüm'}),
            'grade': forms.Select(choices=GRADE, attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=SEX, attrs={'class': 'form-control'}),
        }

        error_messages = {
            'username': ERROR_MESSAGES,
            'email': ERROR_MESSAGES,
            'first_name': ERROR_MESSAGES,
            'last_name': ERROR_MESSAGES,
            'university': ERROR_MESSAGES,
            'department': ERROR_MESSAGES,
            'grade': ERROR_MESSAGES,
            'city': ERROR_MESSAGES,
            'sex': ERROR_MESSAGES,
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 4 or len(username) > 30:
            raise forms.ValidationError(u'Kullanıcı adınız 4 karakterden fazla 30 karakterden az olmalıdır.')

        if username and User.objects.filter(username=username).count():
            raise forms.ValidationError(u'Bu kullanıcı adı başka bir kullanıcı tarafından kullanılmaktadır.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Şifreniz en az 8 karakter olmalıdır.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("Şifrenizi tekrarlamanız gerekmektedir.")
        if password1 != password2:
            raise forms.ValidationError("Girdiğiniz şifreler aynı olmak zorundadır.")
        return password2

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["grade"].choices = [("", "Sınıf")] + list(self.fields["grade"].choices)[1:]
        self.fields["city"].choices = [("", "Şehir")] + list(self.fields["city"].choices)[1:]
        self.fields["sex"].choices = [("", "Cinsiyet")] + list(self.fields["sex"].choices)[1:]

