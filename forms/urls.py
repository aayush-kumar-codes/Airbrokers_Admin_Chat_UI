from django.urls import path
from .views import PDFProcessingView, PDFPostProcessingAPI, PDFUploadListAPI, PDFProcessingDeleteAPI, PDFProcessingSaveAPI, PDFGetProcessingAPI, PDFUpdateProcessingAPI

urlpatterns = [
    path('process_pdf/', PDFProcessingView.as_view(), name='process_pdf'),  # URL for processing PDF
    path('edit-json/<str:file_name>/', PDFProcessingView.as_view(), name='edit_json'),
    path('save-json/', PDFProcessingView.as_view(), name='save_json'),

    path('api/process-pdf/', PDFPostProcessingAPI.as_view(), name='process-pdf-api'),
    path('api/get-all-pdfs/', PDFUploadListAPI.as_view(), name='get-all-pdfs'),
    path('api/process/<int:id>/', PDFGetProcessingAPI.as_view(), name='get_processed_pdf'),
    path('pdf-processing/delete/<int:id>/', PDFProcessingDeleteAPI.as_view(), name='pdf-processing-delete'),
    path('pdf-processing/save/', PDFProcessingSaveAPI.as_view(), name='pdf-processing-save'),
    path('api/update/<int:id>/', PDFUpdateProcessingAPI.as_view(), name='pdf-update-processing'),

]