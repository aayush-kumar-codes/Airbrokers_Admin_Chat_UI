from django import forms
import os
from .models import PDFUpload

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFUpload
        fields = ['input_pdf', 'processed_pdf', 'form_data_json', 'normalized_data_json']

    def clean_input_pdf(self):
        pdf = self.cleaned_data.get('input_pdf')
        if pdf:
            pdf_name = os.path.splitext(pdf.name)[0]
            # Truncate filename if it's longer than 100 characters
            if len(pdf_name) > 100:
                pdf_name = pdf_name[:100]  # Truncate to 100 characters
                new_filename = pdf_name + os.path.splitext(pdf.name)[1]
                # Assign the truncated filename back to the file
                pdf.name = new_filename
        return pdf
