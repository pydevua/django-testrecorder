from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^(\d+)/$', 'news_details', name='news-details')
)