from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register_user'),
    path('login/', views.LoginView.as_view(), name='login_user'),
    path('logout/', views.LogoutView.as_view(), name='logout_user'),
    path('add/', views.AddView.as_view(), name='add_user'),
    path('list/', views.ListView.as_view(), name='list_user'),
    path('update/', views.UpdateView.as_view(), name='update_user'),
    path('delete/', views.DeleteView.as_view(), name='delete_user'),
    path('media/', views.MediaView.as_view(), name='media'),
    path('media/<str:uuid>', views.MediaView.as_view(), name='user_media'),
    path('downloaded-docs/<str:uuid>/', views.DownloadedDocsView.as_view(), name='downloaded_docs'),
    path('uploaded-docs/<str:uuid>/', views.UploadedDocsView.as_view(), name='uploaded_docs'),
    path('docs/', views.DocsView.as_view(), name='user_docs'),
    path('actions/', views.ActionLogsView.as_view(), name='actions'),
    path('actions/<str:uuid>', views.ActionLogsView.as_view(), name='user_actions')
]