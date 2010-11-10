from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import logout, login

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url('^logout/$', logout, {}, 'logout'),
    url('^login/$', login, {}, 'login'),
    (r'^', include('main.urls', 'main')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )