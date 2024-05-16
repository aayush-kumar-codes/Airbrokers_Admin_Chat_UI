from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
    path('status/', views.UpdateChatStatusView.as_view(), name='chat_status'),
    path('send-response/', views.AdminResponseView.as_view(), name='send_response'),
    path('property-chat/', views.PropertyChatUsersListView.as_view(), name='property_chat'),
    path('property-chat/<str:property_id>/<str:user_id>', views.PropertyUserAllChatView.as_view(), name='property_messages')
]