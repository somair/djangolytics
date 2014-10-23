from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', "googleAnalytics.views.index"),
    url(r'^oauth2callback$', "googleAnalytics.views.auth_return"),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', "django.contrib.auth.views.login",
                              {"template_name": "googleAnalytics/login.html"}),
)
