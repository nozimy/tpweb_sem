"""get200 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from asker import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',            views.index, name='index'),
    path('admin/',      admin.site.urls),
    path('login/',      views.login, name='login'),
    path('signup/',     views.signup, name='signup'),
    path('logout/',     views.logout, name="logout"),
    path('ask/', views.ask, name='ask'),
    path('question/<int:qid>/', views.question, name='question'),
    path('profile/',    views.profile, name='profile'),
    path('questions/tagged/<slug:tag>/', views.index, name='tagged'),
    path('answer/<int:question_id>/', views.answer, name='answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
