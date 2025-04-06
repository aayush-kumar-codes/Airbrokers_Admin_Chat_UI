from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PDFUpload
from .views import PDFProcessingView
import os

@receiver(post_save, sender=PDFUpload)
def process_pdf_after_upload(sender, instance, created, **kwargs):
    if created:
        # PDF file has been uploaded, now process it
        input_pdf_path = os.path.join(instance.input_pdf.storage.location, instance.input_pdf.name)

        # Call the process_pdf function to generate JSON files and final editable PDF
        processing_view = PDFProcessingView()
        # Pass 'request' as well if needed; otherwise, we pass the 'input_pdf' path directly
        processing_view.process_pdf(None, input_pdf_path)  # Pass None as 'request' or pass a mock request object if needed
