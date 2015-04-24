from django.conf.urls import patterns, include, url
urlpatterns = patterns('bitirme.views',
    url(r'^$', 'index', name='index')
)
