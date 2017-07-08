from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^profile/([0-9]+)/?$', views.profile, name='admin_profile')
]
