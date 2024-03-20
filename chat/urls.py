from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('status/', views.UpdateChatStatusView.as_view(), name='chat_status'),
    path('send-response/', views.AdminResponseView.as_view(), name='send_response')
]