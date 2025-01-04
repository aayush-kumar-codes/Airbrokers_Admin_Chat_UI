from django.urls import path
from .views import PDFProcessingView  # Your class-based view

urlpatterns = [
    path('process_pdf/', PDFProcessingView.as_view(), name='process_pdf'),  # URL for PDF processing
]
