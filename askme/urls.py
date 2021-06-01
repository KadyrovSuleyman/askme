"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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


from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('ask/', views.ask, name='ask'),
    path('question/<int:pk>/', views.one_question, name='one_question'),
    path('tag/<str:pk>/', views.tag_questions, name="tag_questions"),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.registration, name='registration'),
]
