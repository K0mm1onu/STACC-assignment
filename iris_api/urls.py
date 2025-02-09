"""
URL configuration for iris_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from iris_flowers_api import views

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('flowers', views.FlowerSpecimen.as_view(), name='flowers'),
    path('species', views.FlowerSpecies.as_view(), name='species'),
    path('init-data', views.InitData.as_view(), name='init-data')
]
