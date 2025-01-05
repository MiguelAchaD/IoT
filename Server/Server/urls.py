"""
URL configuration for Server project.

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
from django.contrib import admin
from django.urls import path, include, re_path
from ServerApp.views import dashboard, home, profile, patients, login, register, calendar, addPatient, editPatient, deletePatient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dashboard/<str:id>', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('patients/', patients, name="patients"),
    path('add-patient/<str:public_id>;<str:name>;<str:age>;<str:sex>;<str:city>', addPatient, name="addPatient"),
    path('edit-patient/<str:old_public_id>;<str:public_id>;<str:name>;<str:age>;<str:sex>;<str:city>', editPatient, name="editPatient"),
    path('delete-patient/<str:public_id>', deletePatient, name="deletePatient"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('', home, name="home"),
    path('calendar/', calendar, name='calendar')
]