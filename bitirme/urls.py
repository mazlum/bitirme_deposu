from django.conf.urls import patterns, include, url
urlpatterns = patterns('bitirme.views',
    url(r'^$', 'index', name='index'),
    url(r'^giris/$', 'user_login', name='login'),
    url(r'^cikis/$', 'user_logout', name='logout'),
)
