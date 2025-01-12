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
from ServerApp.views import dashboard, home, profile, patients, login, register, calendar, addPatient, editPatient, deletePatient, logout_view, contact_view, add_reunion, update_reunion, delete_reunion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', home, name="home"),
    path('dashboard/<str:id>', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('patients/', patients, name="patients"),
    path('add-patient/<str:public_id>;<str:name>;<str:age>;<str:sex>;<str:city>', addPatient, name="addPatient"),
    path('edit-patient/<str:old_public_id>;<str:public_id>;<str:name>;<str:age>;<str:sex>;<str:city>', editPatient, name="editPatient"),
    path('delete-patient/<str:public_id>', deletePatient, name="deletePatient"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('calendar/<str:public_id>', calendar, name='calendar'),
    path('add-reunion/<str:title>;<str:start>;<str:description>;<str:url>', add_reunion, name='add_reunion'),
    path('update-reunion/<str:title>;<str:start>;<str:description>;<str:url>', update_reunion, name='update-reunion'),
    path('delete-reunion/<str:title>', delete_reunion, name='delete-reunion'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact_view, name='contact'),
    path('send-message/', contact_view, name='send_message'),
]