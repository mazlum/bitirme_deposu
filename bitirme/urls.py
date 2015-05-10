from django.conf.urls import patterns, include, url

urlpatterns = patterns('bitirme.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^giris/$', 'user_login', name='login'),
                       url(r'^giris-ajax/$', 'user_login_ajax', name='login_ajax'),
                       url(r'^cikis/$', 'user_logout', name='logout'),
                       url(r'^kaydol/$', 'create_account', name='create_account'),
                       url(r'^kaydol-ajax/$', 'create_account_ajax', name='create_account_ajax'),
                       url(r'^hakkinda/$', 'about', name='about'),
                       url(r'^profil/$', 'profile', name='profile'),
                       url(r'^profil-ajax/$', 'profile_ajax', name='profile_edit'),
                       url(r'^user/([A-Za-z0-9]{1,30})/$', 'user_profile', name='user_profile'),
                       url(r'^tez-olustur/$', 'thesis_create', name='thesis_create'),
                       url(r'^tez-olustur-ajax/$', 'thesis_create_ajax', name='thesis_create_ajax'),
)
