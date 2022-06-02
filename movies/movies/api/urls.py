from django.contrib import admin
from django.urls import path
from django.urls import include, path

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]