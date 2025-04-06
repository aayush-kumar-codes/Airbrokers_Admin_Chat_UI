# #############this is full working models for upload_pdf and retribve output#############

# import os
# from django.db import models
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings

# # Custom storage to save files in MEDIA_ROOT/output
# fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'output'))

# def pdf_upload_to(instance, filename):
#     """Store the PDF files in the output folder with their name as the folder."""
#     pdf_name = os.path.splitext(filename)[0]
#     # Truncate filename if it's longer than 100 characters
#     if len(pdf_name) > 100:
#         pdf_name = pdf_name[:100]  # Truncate to 100 characters
#     return os.path.join('output', f'{pdf_name}{os.path.splitext(filename)[1]}')

# class PDFUpload(models.Model):
#     input_pdf = models.FileField(upload_to=pdf_upload_to, storage=fs)  # Use custom upload function
#     processed_pdf = models.FileField(upload_to='output/', null=True, blank=True)
#     form_data_json = models.FileField(upload_to='output/', null=True, blank=True)
#     normalized_data_json = models.FileField(upload_to='output/', null=True, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.input_pdf.name

#     def save(self, *args, **kwargs):
#         # Ensure this is a new record, then save
#         if not self.pk:  # If pk is None, it's a new record
#             super().save(*args, **kwargs)  # Save initially to generate pk
        
#         # Process the PDF and save the output only for new files
#         if self.input_pdf and not self.processed_pdf:
#             self.process_pdf()

#         super().save(*args, **kwargs)  # Save the new record with processed data

#     def process_pdf(self):
#         """Process the PDF file and store related files in a folder named after the input PDF."""
#         output_folder = self.setup_folders()  # Create a unique folder for this PDF
        
#         # Ensure the filenames are within 100 characters (including extension)
#         processed_pdf_name = f'final_form.pdf'
#         form_data_json_name = f'form_data.json'
#         normalized_data_json_name = f'normalized_form_data.json'

#         # Remove extra .json.json extension if it exists
#         if form_data_json_name.endswith('.json.json'):
#             form_data_json_name = form_data_json_name[:-5]  
#         if normalized_data_json_name.endswith('.json.json'):
#             normalized_data_json_name = normalized_data_json_name[:-5]

#         # Save the files in the correct folder
#         self.processed_pdf = os.path.join('output', f'{os.path.basename(output_folder)}/final_form.pdf')
#         self.form_data_json = os.path.join('output', f'{os.path.basename(output_folder)}/form_data.json')
#         self.normalized_data_json = os.path.join('output', f'{os.path.basename(output_folder)}/normalized_form_data.json')

#     def setup_folders(self):
#         """Create a unique folder inside MEDIA_ROOT based on the input PDF name."""
#         # Use the base name of the PDF (without extension) to create the folder
#         pdf_name = os.path.splitext(self.input_pdf.name)[0]
        
#         # This will ensure that the folder name is exactly the same as the input PDF name
#         folder_name = pdf_name
#         output_folder = os.path.join(settings.MEDIA_ROOT, 'output', folder_name)
#         os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
#         return output_folder


#############this is full working models for upload_pdf and retribve output#############



###################working with good file path##################

import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Custom storage to save files in MEDIA_ROOT/output
fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'output'))

def pdf_upload_to(instance, filename):
    """Store the PDF files in the output folder with their name as the folder."""
    pdf_name = os.path.splitext(filename)[0]
    # Truncate filename if it's longer than 100 characters
    if len(pdf_name) > 100:
        pdf_name = pdf_name[:100]  # Truncate to 100 characters
    return os.path.join('output', f'{pdf_name}{os.path.splitext(filename)[1]}')

class PDFUpload(models.Model):
    input_pdf = models.FileField(upload_to=pdf_upload_to, storage=fs)  # Use custom upload function
    processed_pdf = models.FileField(upload_to='output/', null=True, blank=True)
    form_data_json = models.FileField(upload_to='output/', null=True, blank=True)
    normalized_data_json = models.FileField(upload_to='output/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.input_pdf.name

    def save(self, *args, **kwargs):
        # Ensure this is a new record, then save
        if not self.pk:  # If pk is None, it's a new record
            super().save(*args, **kwargs)  # Save initially to generate pk
        
        # Process the PDF and save the output only for new files
        if self.input_pdf and not self.processed_pdf:
            self.process_pdf()

        super().save(*args, **kwargs)  # Save the new record with processed data

    def process_pdf(self):
        """Process the PDF file and store related files in a folder named after the input PDF."""
        output_folder = self.setup_folders()  # Create a unique folder for this PDF
        
        # Ensure the filenames are within 100 characters (including extension)
        processed_pdf_name = f'final_form.pdf'
        form_data_json_name = f'form_data.json'
        normalized_data_json_name = f'normalized_form_data.json'

        # Remove extra .json.json extension if it exists
        if form_data_json_name.endswith('.json.json'):
            form_data_json_name = form_data_json_name[:-5]  
        if normalized_data_json_name.endswith('.json.json'):
            normalized_data_json_name = normalized_data_json_name[:-5]

        # Save the files in the correct folder
        self.processed_pdf = os.path.join('output', f'{os.path.basename(output_folder)}/final_form.pdf')
        self.form_data_json = os.path.join('output', f'{os.path.basename(output_folder)}/form_data.json')
        self.normalized_data_json = os.path.join('output', f'{os.path.basename(output_folder)}/normalized_form_data.json')
        
        # Save the input_pdf in the same folder
        self.input_pdf.name = os.path.join(f'output/{os.path.basename(output_folder)}', os.path.basename(self.input_pdf.name))

    def setup_folders(self):
        """Create a unique folder inside MEDIA_ROOT based on the input PDF name."""
        # Use the base name of the PDF (without extension) to create the folder
        pdf_name = os.path.splitext(self.input_pdf.name)[0]
        
        # This will ensure that the folder name is exactly the same as the input PDF name
        folder_name = pdf_name
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output', folder_name)
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        return output_folder
