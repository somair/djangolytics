from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', "googleAnalytics.views.index"),
    url(r'^hit_api$', "googleAnalytics.views.hit_api"),
    url(r'^pick_date$', "googleAnalytics.views.select_date"),
    url(r'^dot_chart$', "googleAnalytics.views.dot_chart"),
    url(r'^oauth2callback$', "googleAnalytics.views.auth_return"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', "django.contrib.auth.views.login",
                              {"template_name": "googleAnalytics/login.html"}),
)
