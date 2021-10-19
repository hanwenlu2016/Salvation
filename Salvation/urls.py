"""Salvation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from api.urls import router
from element.views.element_wiews import ElementListView

urlpatterns = [
    path('admin/', admin.site.urls, ),
    path('api-token-auth/', views.obtain_auth_token, name='auth-token'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('oauth.urls')),
    path('api/', include(router.urls)),
    path('project/', include('project.urls')),
    path('tool/', include('tool.urls')),
    path('eln/', ElementListView.as_view(), name='eln'),
]

handler400 = 'oauth.views.error_views.bad_request'
handler403 = 'oauth.views.error_views.permission_denied'
handler404 = 'oauth.views.error_views.page_not_found'
handler500 = 'oauth.views.error_views.server_error'
