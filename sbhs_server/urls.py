from django.conf.urls import include, url
from django.contrib import admin

# from django.contrib import custom_admin
# custom_admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'sbhs_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exam/', include('yaksh.urls')),
    url(r'^', include('pages.urls')),
    url(r'^', include('account.urls')),
    url(r'^password/', include('password.urls')),
    url(r'^', include('experiment.urls')),
    url(r'^', include('custom_admin.urls')),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
]

handler404 = 'pages.views.e404'
handler500 = 'pages.views.e500'
