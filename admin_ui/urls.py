"""
URL configuration for admin_ui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('users/', include('users.urls')),
    #path('templates/', views.DocumentsView.as_view(), name='templates'),
    path('documents/', views.AllDocumentsView.as_view(), name='documents'),
    path('update-document/', views.UpdateDocumentView.as_view(), name='update_document'),
    path('chats/', include('chat.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
