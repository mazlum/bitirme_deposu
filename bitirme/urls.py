from django.conf.urls import patterns, include, url
urlpatterns = patterns('bitirme.views',
    url(r'^$', 'index', name='index'),
    url(r'^giris/$', 'user_login', name='login'),
    url(r'^giris-ajax/$', 'user_login_ajax', name='login_ajax'),
    url(r'^cikis/$', 'user_logout', name='logout'),
    url(r'^hesap-olustur/$', 'create_account', name='create_account'),
    url(r'^hesap-olustur-ajax/$', 'create_account_ajax', name='create_account_ajax'),
)
