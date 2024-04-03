from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('fl-forms/', views.FlFormsView.as_view(), name='flforms'),
    path('fl-forms/<filename>/<folder>', views.SingleFlFormsView.as_view(), name='single_flforms'),
    path('mn-forms/', views.MnFormsView.as_view(), name='mnforms'),
    path('mn-forms/<filename>/<folder>', views.SingleMnFormsView.as_view(), name='single_mnforms'),
    path('documents/', views.AllDocumentsView.as_view(), name='documents'),
    path('update-document/', views.UpdateDocumentView.as_view(), name='update_document'),
    path('upload-document/', views.UploadDocumentView.as_view(), name='upload_document'),
    path('flforms/move/', views.MoveFlFormsDocumentView.as_view(), name='move_flforms'),
    path('mnforms/move/', views.MoveMnFormsDocumentView.as_view(), name='move_mnforms'),
]