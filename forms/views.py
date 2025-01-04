import os
import json
import time
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .files.form_processor import FormProcessor
from .files.structured_processor import StructuredFormProcessor
from .files.normalize import normalize_form_data
from .files.form_generator import create_acroform_from_images, get_image_files_from_folder

class PDFProcessingView(View):

    def setup_folders(self):
        # Ensure the output folder exists inside MEDIA_ROOT
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output')
        os.makedirs(output_folder, exist_ok=True)
        print(f"Created folder: {output_folder}")
        return output_folder
    
    def process_pdf(self, input_pdf: str, output_folder: str = None) -> dict:
        if not output_folder:
            output_folder = self.setup_folders()

        start_time = time.time()
        try:
            # Validate input file
            if not os.path.exists(input_pdf):
                raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
            
            # Process form elements
            print(f"\nProcessing PDF: {input_pdf}")
            processor = FormProcessor(output_folder)
            results = processor.process_pdf(input_pdf)
            
            # Generate structured data
            print("\nGenerating structured data...")
            structured_processor = StructuredFormProcessor()
            structured_processor.process_pdf_metadata(input_pdf)
            structured_processor.process_form_data(results)
            
            # Save form data
            form_data_path = Path(output_folder) / 'form_data.json'
            structured_processor.save_json(str(form_data_path))
            print(f"Form data saved to: {form_data_path}")
           
            # Normalize coordinates
            print("\nNormalizing coordinates...")
            with open(form_data_path) as f:
                form_data = json.load(f)
                image_path = Path(output_folder) / 'page_1.png'  # Define image_path
                normalized_data = normalize_form_data(image_path, input_pdf, form_data)
            
            # Save normalized data
            normalized_path = Path(output_folder) / 'normalized_form_data.json'
            with open(normalized_path, 'w') as f:
                json.dump(normalized_data, f, indent=2)
            print(f"Normalized data saved to: {normalized_path}")
            
            # Generate fillable PDF
            print("\nGenerating fillable PDF form...")
            image_files = get_image_files_from_folder(output_folder)
            output_pdf = Path(output_folder) / 'final_form.pdf'
            
            # Get page dimensions from structured data
            with open(normalized_path) as f:
                normalized_data = json.load(f)
                page_dimensions = normalized_data.get('page_dimensions')
            
            create_acroform_from_images(
                image_files, 
                str(normalized_path), 
                str(output_pdf),
                page_dimensions
            )
            print(f"Fillable PDF created: {output_pdf}")
            
            return {
                "status": "success",
                "message": f"Fillable PDF created: {output_pdf}",
                "file": str(output_pdf)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing PDF: {str(e)}"
            }
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time taken to process PDF: {elapsed_time:.2f} seconds")

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        input_pdf = request.FILES.get('input_pdf')  # Get the uploaded PDF file from request
        
        if input_pdf:
            output_folder = self.setup_folders()  # Create output folder under MEDIA_ROOT
            input_pdf_path = os.path.join(output_folder, input_pdf.name)
            
            # Save the uploaded file to a temporary location
            with open(input_pdf_path, 'wb') as f:
                for chunk in input_pdf.chunks():
                    f.write(chunk)
            
            result = self.process_pdf(input_pdf_path, output_folder)
            return JsonResponse(result)
        
        return JsonResponse({"status": "error", "message": "No input PDF provided"}, status=400)