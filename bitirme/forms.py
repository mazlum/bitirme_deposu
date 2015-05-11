# -*- coding: utf-8 -*-
from django.contrib.auth.forms import forms, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.utils.encoding import force_bytes
from models import Users, Thesis, File, Image, GRADE, SEX
from multiupload.fields import MultiFileField
from validators import validate_multi_thesis_file, validate_multi_image_file

ERROR_MESSAGES = {
    'invalid': u'Bu alan için geçersiz değer girdiniz.',
    'required': u'Bu alan zorunludur.',
}


class LoginForm(AuthenticationForm):
    captcha = NoReCaptchaField(ERROR_MESSAGES,
                               gtag_attrs={'data-theme': 'dark'})
    username = forms.CharField(
        error_messages={'required': 'Kullanıcı adı zorunludur', 'invalid': 'Geçersiz kullanıcı adı'},
        label='Kullanıcı Adı', widget=forms.TextInput(attrs={'class': 'form-control input-lg',
                                                             'placeHolder': 'Kullanıcı adı'}))
    password = forms.CharField(error_messages={'required': 'Şifre zorunludur', 'invalid': 'Geçersiz şifre'},
                               label='Şifre', widget=forms.PasswordInput(attrs={'class': 'form-control input-lg',
                                                                                'placeHolder': 'Şifre'}))

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
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class ThesisAdminForm(forms.ModelForm):
    def clean_file(self):
        get_file = self.cleaned_data.get('file')
        if get_file.count() > 5:
            raise forms.ValidationError("File number should be at least 5")
        return get_file

    def clean_image(self):
        get_image = self.cleaned_data.get('image')
        if get_image.count() > 5:
            raise forms.ValidationError("Image number should be at least 5")
        return get_image


class RegisterForm(UserCreationForm):
    captcha = NoReCaptchaField(error_messages=ERROR_MESSAGES, gtag_attrs={'data-theme': 'dark'})
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Bu mail adresi başka bir kullanıcı tarafından kullanılmaktadır.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 4 or len(username) > 30:
            raise forms.ValidationError(u'Kullanıcı adınız 4 karakterden fazla 30 karakterden az olmalıdır.')

        if username and User.objects.filter(username=username).exists():
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
        self.fields["grade"].choices = [("", "Sınıf Seçiniz")] + list(self.fields["grade"].choices)[1:]
        self.fields["city"].choices = [("", "Şehir Seçiniz")] + list(self.fields["city"].choices)[1:]
        self.fields["sex"].choices = [("", "Cinsiyet Seçiniz")] + list(self.fields["sex"].choices)[1:]
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class EditProfileForm(forms.ModelForm):
    captcha = NoReCaptchaField(error_messages=ERROR_MESSAGES, gtag_attrs={'data-theme': 'dark'})

    class Meta:
        model = Users
        fields = ['image', 'username', 'email', 'first_name', 'last_name', 'university', 'department', 'grade',
                  'city', 'sex']

        widgets = {
            'image': forms.FileInput(),
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

        if username and User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(u'Bu kullanıcı adı başka bir kullanıcı tarafından kullanılmaktadır.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(u'Bu mail adresi başka bir kullanıcı tarafından kullanılmaktadır.')
        return email

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["grade"].choices = [("", "Sınıf Seçiniz")] + list(self.fields["grade"].choices)[1:]
        self.fields["city"].choices = [("", "Şehir Seçiniz")] + list(self.fields["city"].choices)[1:]
        self.fields["sex"].choices = [("", "Cinsiyet Seçiniz")] + list(self.fields["sex"].choices)[1:]
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['name', 'content']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeHolder': 'Tez Başlığı'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeHolder': 'Tez Açıklaması'}),
        }
        error_messages = {
            'name': ERROR_MESSAGES,
            'content': ERROR_MESSAGES,
        }

    file_error_messages = {
        'invalid': u'Geçersiz değer girdiniz.',
        'required': u'Bu alan zorunludur.',
        'min_num': u'En az %(min_num) sayıda yükleme yapmalısınız.',
        'max_num': u'En fazla %(max_num) sayoda yükleme yapabilirsiniz.',
        'file_size': u' %(uploaded_file_name)s isimli dosya  çok büyük. En fazla 5 MB yükleyebilirsiniz.',
    }

    files = MultiFileField(min_num=1, max_num=5, max_file_size=1024*1024*5, validators=[validate_multi_thesis_file],
                           error_messages=file_error_messages)
    images = MultiFileField(min_num=1, max_num=5, max_file_size=1024*1024*5, validators=[validate_multi_image_file],
                            error_messages=file_error_messages)

    captcha = NoReCaptchaField(error_messages=ERROR_MESSAGES, gtag_attrs={'data-theme': 'dark'})
