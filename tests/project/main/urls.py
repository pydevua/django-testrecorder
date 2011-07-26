from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^send_email/$', 'send_email', name='send_email'),
    url(r'^(\d+)/$', 'news_details', name='news-details'),
)