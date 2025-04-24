"""
URL configuration for ticketing_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path



# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ticketing_system.views import *

router = DefaultRouter()
router.register(prefix=r'users', viewset=UserViewset, basename='users')
router.register(prefix=r'dashboard', viewset=DashBoardViewSet, basename='dashboard')
router.register(prefix=r'ticket', viewset=TicketViewset, basename='ticket')
router.register(prefix=r'projects', viewset=ProjectViewset, basename='projects')

urlpatterns = [
    path('ticketing_sys/', include(router.urls)),
]
