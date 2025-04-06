# import os
# import json
# import time
# from pathlib import Path
# from django.conf import settings
# from django.http import JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from .files.form_processor import FormProcessor
# from .files.structured_processor import StructuredFormProcessor
# from .files.normalize import normalize_form_data
# from .files.form_generator import create_acroform_from_images, get_image_files_from_folder

# class PPDFProcessingView(View):

#     def setup_folders(self):
#         # Ensure the output folder exists inside MEDIA_ROOT
#         output_folder = os.path.join(settings.MEDIA_ROOT, 'output')
#         os.makedirs(output_folder, exist_ok=True)
#         print(f"Created folder: {output_folder}")
#         return output_folder
    
#     def process_pdf(self, input_pdf: str, output_folder: str = None) -> dict:
#         if not output_folder:
#             output_folder = self.setup_folders()

#         start_time = time.time()
#         try:
#             # Validate input file
#             if not os.path.exists(input_pdf):
#                 raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
            
#             # Process form elements
#             print(f"\nProcessing PDF: {input_pdf}")
#             processor = FormProcessor(output_folder)
#             results = processor.process_pdf(input_pdf)
            
#             # Generate structured data
#             print("\nGenerating structured data...")
#             structured_processor = StructuredFormProcessor()
#             structured_processor.process_pdf_metadata(input_pdf)
#             structured_processor.process_form_data(results)
            
#             # Save form data
#             form_data_path = Path(output_folder) / 'form_data.json'
#             structured_processor.save_json(str(form_data_path))
#             print(f"Form data saved to: {form_data_path}")
           
#             # Normalize coordinates
#             print("\nNormalizing coordinates...")
#             with open(form_data_path) as f:
#                 form_data = json.load(f)
#                 image_path = Path(output_folder) / 'page_1.png'  # Define image_path
#                 normalized_data = normalize_form_data(image_path, input_pdf, form_data)
            
#             # Save normalized data
#             normalized_path = Path(output_folder) / 'normalized_form_data.json'
#             with open(normalized_path, 'w') as f:
#                 json.dump(normalized_data, f, indent=2)
#             print(f"Normalized data saved to: {normalized_path}")
            
#             # Generate fillable PDF
#             print("\nGenerating fillable PDF form...")
#             image_files = get_image_files_from_folder(output_folder)
#             output_pdf = Path(output_folder) / 'final_form.pdf'
            
#             # Get page dimensions from structured data
#             with open(normalized_path) as f:
#                 normalized_data = json.load(f)
#                 page_dimensions = normalized_data.get('page_dimensions')
            
#             create_acroform_from_images(
#                 image_files, 
#                 str(normalized_path), 
#                 str(output_pdf),
#                 page_dimensions
#             )
#             print(f"Fillable PDF created: {output_pdf}")
            
#             return {
#                 "status": "success",
#                 "message": f"Fillable PDF created: {output_pdf}",
#                 "file": str(output_pdf)
#             }

#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"Error processing PDF: {str(e)}"
#             }
#         finally:
#             end_time = time.time()
#             elapsed_time = end_time - start_time
#             print(f"Time taken to process PDF: {elapsed_time:.2f} seconds")

#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         input_pdf = request.FILES.get('input_pdf')  # Get the uploaded PDF file from request
        
#         if input_pdf:
#             output_folder = self.setup_folders()  # Create output folder under MEDIA_ROOT
#             input_pdf_path = os.path.join(output_folder, input_pdf.name)
            
#             # Save the uploaded file to a temporary location
#             with open(input_pdf_path, 'wb') as f:
#                 for chunk in input_pdf.chunks():
#                     f.write(chunk)
            
#             result = self.process_pdf(input_pdf_path, output_folder)
#             return JsonResponse(result)
        
#         return JsonResponse({"status": "error", "message": "No input PDF provided"}, status=400)

# # ###############uper is for API#############################




# # import os
# # import time
# # import json
# # from pathlib import Path
# # from django.conf import settings
# # from django.http import JsonResponse
# # from .models import PDFUpload
# # from django.shortcuts import render
# # from django.views import View
# # from django.views.decorators.csrf import csrf_exempt
# # from .files.form_processor import FormProcessor
# # from .files.structured_processor import StructuredFormProcessor
# # from .files.normalize import normalize_form_data
# # from .files.form_generator import create_acroform_from_images, get_image_files_from_folder
# # class PDFProcessingView(View):

# #     def setup_folders(self, input_pdf: str):
# #         """Create a unique folder based on the input PDF's name inside MEDIA_ROOT."""
# #         pdf_name = os.path.splitext(os.path.basename(input_pdf))[0]
        
# #         if len(pdf_name) > 100:
# #             pdf_name = pdf_name[:100]  # Truncate if name is too long
        
# #         # Create the folder inside the output directory
# #         output_folder = os.path.join(settings.MEDIA_ROOT, f'output/{pdf_name}')
# #         os.makedirs(output_folder, exist_ok=True)
# #         return output_folder

# #     def process_pdf(self, request, input_pdf: str) -> dict:
# #         try:
# #             # Generate a unique folder based on the input PDF name
# #             output_folder = self.setup_folders(input_pdf)
            
# #             # Validate input file
# #             if not os.path.exists(input_pdf):
# #                 raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
            
# #             # Process the form elements and save in the generated folder
# #             processor = FormProcessor(output_folder)
# #             results = processor.process_pdf(input_pdf)
            
# #             structured_processor = StructuredFormProcessor()
# #             structured_processor.process_pdf_metadata(input_pdf)
# #             structured_processor.process_form_data(results)
            
# #             # Save the JSON files in the correct folder
# #             form_data_path = os.path.join(output_folder, 'form_data.json')
# #             structured_processor.save_json(str(form_data_path))
           
# #             # Normalize coordinates
# #             with open(form_data_path) as f:
# #                 form_data = json.load(f)
# #                 image_path = os.path.join(output_folder, 'page_1.png')  # Path to image for normalization
# #                 normalized_data = normalize_form_data(image_path, input_pdf, form_data)
            
# #             normalized_path = os.path.join(output_folder, 'normalized_form_data.json')
# #             with open(normalized_path, 'w') as f:
# #                 json.dump(normalized_data, f, indent=2)
            
# #             # Generate final PDF
# #             image_files = get_image_files_from_folder(output_folder)
# #             output_pdf = os.path.join(output_folder, 'final_form.pdf')
            
# #             with open(normalized_path) as f:
# #                 normalized_data = json.load(f)
# #                 page_dimensions = normalized_data.get('page_dimensions')
            
# #             create_acroform_from_images(image_files, str(normalized_path), str(output_pdf), page_dimensions)
            
# #             # Prepare response data
# #             result = {
# #                 "status": "success",
# #                 "message": f"Fillable PDF created: {output_pdf}",
# #                 "file": f"/media/output/{os.path.basename(output_folder)}/final_form.pdf",  # URL for the PDF
# #                 "form_data": f"/media/output/{os.path.basename(output_folder)}/form_data.json",  # URL for JSON
# #                 "normalized_data": f"/media/output/{os.path.basename(output_folder)}/normalized_form_data.json"  # URL for JSON
# #             }

# #             return render(request, 'forms/output.html', {'result': result})

# #         except Exception as e:
# #             result = {
# #                 "status": "error",
# #                 "message": f"Error processing PDF: {str(e)}"
# #             }
# #             return render(request, 'forms/output.html', {'result': result})




from django.http import JsonResponse
from django.shortcuts import render
import json
import os
from django.conf import settings
from django.views import View

import os
import json
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .files.form_processor import FormProcessor
from .files.structured_processor import StructuredFormProcessor
from .files.normalize import normalize_form_data
from .files.form_generator import create_acroform_from_images, get_image_files_from_folder
from django.core.files.storage import FileSystemStorage

class PDFProcessingView(View):

    def setup_folders(self, input_pdf: str):
        """Create a unique folder based on the input PDF's name inside MEDIA_ROOT."""
        pdf_name = os.path.splitext(os.path.basename(input_pdf))[0]
        
        if len(pdf_name) > 100:
            pdf_name = pdf_name[:100]  # Truncate if name is too long
        
        # Create the folder inside the output directory under MEDIA_ROOT
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output', pdf_name)  # Correct path
        os.makedirs(output_folder, exist_ok=True)  # Create the folder
        return output_folder

    def process_pdf(self, request, input_pdf: str) -> dict:
        try:
            # Generate a unique folder based on the input PDF name
            output_folder = self.setup_folders(input_pdf)
            
            # Validate input file
            if not os.path.exists(input_pdf):
                raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
            
            # Save the input PDF in the correct folder
            fs = FileSystemStorage(location=output_folder)
            fs.save(os.path.basename(input_pdf), open(input_pdf, 'rb'))

            # Process the form elements and save in the generated folder
            processor = FormProcessor(output_folder)
            results = processor.process_pdf(input_pdf)
            
            structured_processor = StructuredFormProcessor()
            structured_processor.process_pdf_metadata(input_pdf)
            structured_processor.process_form_data(results)
            print("structured_processor",structured_processor)
            print(output_folder)
            # Save the JSON files in the correct folder
            form_data_path = os.path.join(output_folder, 'form_data.json')
            structured_processor.save_json(str(form_data_path))
           
            # Normalize coordinates
            with open(form_data_path) as f:
                form_data = json.load(f)
                image_path = os.path.join(output_folder, 'page_1.png')  # Path to image for normalization
                normalized_data = normalize_form_data(image_path, input_pdf, form_data)
            
            normalized_path = os.path.join(output_folder, 'normalized_form_data.json')
            with open(normalized_path, 'w') as f:
                json.dump(normalized_data, f, indent=2)
            
            # Generate final PDF
            image_files = get_image_files_from_folder(output_folder)
            output_pdf = os.path.join(output_folder, 'final_form.pdf')
            
            with open(normalized_path) as f:
                normalized_data = json.load(f)
                page_dimensions = normalized_data.get('page_dimensions')
            
            create_acroform_from_images(image_files, str(normalized_path), str(output_pdf), page_dimensions)
            
            # Prepare response data
            result = {
                "status": "success",
                "message": f"Fillable PDF created: {output_pdf}",
                # URL for the input PDF
                "input_pdf": f"/media/output/{os.path.basename(output_folder)}/{os.path.basename(input_pdf)}",
                # URL for the generated files
                "file": f"/media/output/{os.path.basename(output_folder)}/final_form.pdf",  # URL for the generated PDF
                "form_data": f"/media/output/{os.path.basename(output_folder)}/form_data.json",  # URL for JSON
                "normalized_data": f"/media/output/{os.path.basename(output_folder)}/normalized_form_data.json"  # URL for JSON
            }
            return render(request, 'forms/output.html', {'result': result})

        except Exception as e:
            result = {
                "status": "error",
                "message": f"Error processing PDF: {str(e)}"
            }
            return render(request, 'forms/output.html', {'result': result})

    def edit_json(self, request, file_name):
        """View to edit the JSON files (form_data.json or normalized_form_data.json)."""
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, 'output', file_name)

            if not os.path.exists(file_path):
                return JsonResponse({"error": "File not found"}, status=404)

            with open(file_path, 'r') as f:
                json_data = json.load(f)

            # Return the JSON data for editing
            return JsonResponse({"json_data": json_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

    def save_json(self, request):
        try:
            data = json.loads(request.body)
            file_name = data.get('file_name')
            json_data = data.get('json_data')

            # Define the path where the JSON file should be saved
            file_path = os.path.join(settings.MEDIA_ROOT, 'output', file_name)

            if not os.path.exists(file_path):
                return JsonResponse({"error": "File not found"}, status=404)

            with open(file_path, 'w') as f:
                json.dump(json_data, f, indent=2)

            return JsonResponse({"status": "success"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


#########################



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import os
# import json
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from django.core.exceptions import ValidationError
# from .files.form_processor import FormProcessor
# from .files.structured_processor import StructuredFormProcessor
# from .files.normalize import normalize_form_data
# from .files.form_generator import create_acroform_from_images, get_image_files_from_folder

# class DFProcessingAPI(APIView):
    
#     def setup_folders(self, input_pdf: str):
#         """Create a unique folder based on the input PDF's name inside MEDIA_ROOT."""
#         pdf_name = os.path.splitext(os.path.basename(input_pdf))[0]
        
#         if len(pdf_name) > 100:
#             pdf_name = pdf_name[:100]  # Truncate if name is too long
        
#         # Create the folder inside the output directory under MEDIA_ROOT
#         output_folder = os.path.join(settings.MEDIA_ROOT, 'output', pdf_name)
#         os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
#         return output_folder
    
#     def post(self, request, *args, **kwargs):
#         """Handle the POST request for processing PDF."""
#         # Check if the file is provided in the request
#         if 'file' not in request.FILES:
#             return Response({"status": "error", "message": "No file provided."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         pdf_file = request.FILES['file']
        
#         # Check if it's a PDF
#         if not pdf_file.name.endswith('.pdf'):
#             return Response({"status": "error", "message": "Invalid file type. Only PDF files are allowed."},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             # Save the uploaded PDF to a temporary location
#             fs = FileSystemStorage(location=settings.MEDIA_ROOT)
#             pdf_path = fs.save(pdf_file.name, pdf_file)
#             input_pdf = os.path.join(settings.MEDIA_ROOT, pdf_path)

#             # Generate a unique folder based on the input PDF name
#             output_folder = self.setup_folders(input_pdf)
            
#             # Process the form elements and save in the generated folder
#             processor = FormProcessor(output_folder)
#             results = processor.process_pdf(input_pdf)
            
#             # Process form metadata and structured data
#             structured_processor = StructuredFormProcessor()
#             structured_processor.process_pdf_metadata(input_pdf)
#             structured_processor.process_form_data(results)

#             # Save the JSON files
#             form_data_path = os.path.join(output_folder, 'form_data.json')
#             structured_processor.save_json(str(form_data_path))

#             # Normalize coordinates
#             with open(form_data_path) as f:
#                 form_data = json.load(f)
#                 image_path = os.path.join(output_folder, 'page_1.png')  # Path to image for normalization
#                 normalized_data = normalize_form_data(image_path, input_pdf, form_data)
            
#             # Save the normalized data to JSON
#             normalized_path = os.path.join(output_folder, 'normalized_form_data.json')
#             with open(normalized_path, 'w') as f:
#                 json.dump(normalized_data, f, indent=2)
            
#             # Generate final PDF from the images
#             image_files = get_image_files_from_folder(output_folder)
#             output_pdf = os.path.join(output_folder, 'final_form.pdf')
            
#             with open(normalized_path) as f:
#                 normalized_data = json.load(f)
#                 page_dimensions = normalized_data.get('page_dimensions')
            
#             create_acroform_from_images(image_files, str(normalized_path), str(output_pdf), page_dimensions)
            
#             # Prepare the response with URLs to the generated files
#             result = {
#                 "status": "success",
#                 "message": "Fillable PDF created",
#                 "input_pdf": f"/media/output/{os.path.basename(output_folder)}/{os.path.basename(input_pdf)}",
#                 "file": f"/media/output/{os.path.basename(output_folder)}/final_form.pdf",  # URL for the generated PDF
#                 "form_data": f"/media/output/{os.path.basename(output_folder)}/form_data.json",  # URL for JSON
#                 "normalized_data": f"/media/output/{os.path.basename(output_folder)}/normalized_form_data.json"  # URL for JSON
#             }
#             return Response(result, status=status.HTTP_200_OK)

#         except FileNotFoundError as e:
#             return Response({"status": "error", "message": f"Input PDF not found: {str(e)}"},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         except ValidationError as e:
#             return Response({"status": "error", "message": f"Validation error: {str(e)}"},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as e:
#             return Response({"status": "error", "message": f"Error processing PDF: {str(e)}"},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from .models import PDFUpload
from .files.form_processor import FormProcessor
from .files.structured_processor import StructuredFormProcessor
from .files.normalize import normalize_form_data
from .files.form_generator import create_acroform_from_images, get_image_files_from_folder
from django.db import IntegrityError

class PDFPostProcessingAPI(APIView):

    def setup_folders(self, input_pdf: str):
        """Create a unique folder based on the input PDF's name inside MEDIA_ROOT."""
        pdf_name = os.path.splitext(os.path.basename(input_pdf))[0]

        if len(pdf_name) > 100:
            pdf_name = pdf_name[:100]  # Truncate if name is too long

        # Create the folder inside the output directory under MEDIA_ROOT
        output_folder = os.path.join(settings.MEDIA_ROOT, 'output', pdf_name)
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        return output_folder

    def post(self, request, *args, **kwargs):
        print("kjhg")
        """Handle the POST request for processing PDF."""
        # Check if the file is provided in the request
        if 'file' not in request.FILES:
            return Response({"status": "error", "message": "No file provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        pdf_file = request.FILES['file']

        # Check if it's a PDF
        if not pdf_file.name.endswith('.pdf'):
            return Response({"status": "error", "message": "Invalid file type. Only PDF files are allowed."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Save the uploaded PDF to a temporary location
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            pdf_path = fs.save(pdf_file.name, pdf_file)
            input_pdf = os.path.join(settings.MEDIA_ROOT, pdf_path)

            # Generate a unique folder based on the input PDF name
            output_folder = self.setup_folders(input_pdf)

            # Process the form elements and save in the generated folder
            processor = FormProcessor(output_folder)
            results = processor.process_pdf(input_pdf)

            # Process form metadata and structured data
            structured_processor = StructuredFormProcessor()
            structured_processor.process_pdf_metadata(input_pdf)
            structured_processor.process_form_data(results)

            # Save the JSON files
            form_data_path = os.path.join(output_folder, 'form_data.json')
            structured_processor.save_json(str(form_data_path))

            # Normalize coordinates
            with open(form_data_path) as f:
                form_data = json.load(f)
                image_path = os.path.join(output_folder, 'page_1.png')  # Path to image for normalization
                normalized_data = normalize_form_data(image_path, input_pdf, form_data)

            # Save the normalized data to JSON
            normalized_path = os.path.join(output_folder, 'normalized_form_data.json')
            with open(normalized_path, 'w') as f:
                json.dump(normalized_data, f, indent=2)

            # Generate final PDF from the images
            image_files = get_image_files_from_folder(output_folder)
            output_pdf = os.path.join(output_folder, 'final_form.pdf')

            with open(normalized_path) as f:
                normalized_data = json.load(f)
                page_dimensions = normalized_data.get('page_dimensions')

            create_acroform_from_images(image_files, str(normalized_path), str(output_pdf), page_dimensions)

            # Prepare the response with URLs to the generated files
            result = {
                "status": "success",
                "message": "Fillable PDF created",
                # Fixing the input_pdf path to be relative to MEDIA_URL
                "input_pdf": f"/media/output/{os.path.basename(output_folder)}/{os.path.basename(input_pdf)}",
                # Generating URLs for other files as well
                "file": f"/media/output/{os.path.basename(output_folder)}/final_form.pdf",  # URL for the generated PDF
                "form_data": f"/media/output/{os.path.basename(output_folder)}/form_data.json",  # URL for JSON
                "normalized_data": f"/media/output/{os.path.basename(output_folder)}/normalized_form_data.json"  # URL for JSON
            }
            print(result)
            # Attempt to save the output paths into the PDFUpload model (SQLite)
            try:
                pdf_upload = PDFUpload.objects.create(
                    input_pdf=pdf_path, 
                    processed_pdf=f"output/{os.path.basename(output_folder)}/final_form.pdf",  # Relative path
                    form_data_json=f"output/{os.path.basename(output_folder)}/form_data.json",  # Relative path
                    normalized_data_json=f"output/{os.path.basename(output_folder)}/normalized_form_data.json",  # Store normalized JSON path
                )
                result['database_entry_id'] = pdf_upload.id  # Adding the saved record's ID
            except IntegrityError:
                print("in except")
                # Ignore the error and proceed (in case of unique constraint failure)
                result['message'] += " However, the record already exists in the database."

            return Response(result, status=status.HTTP_200_OK)

        except FileNotFoundError as e:
            print("filenot")
            return Response({"status": "error", "message": f"Input PDF not found: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("exccccccc")
            return Response({"status": "error", "message": f"Error processing PDF: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#############################################


######################################################

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import PDFUpload

class PDFUploadListAPI(APIView):
    """
    API endpoint to retrieve all PDF uploads without using a serializer.
    """
    def get(self, request, *args, **kwargs):
        # Fetch all records from the PDFUpload model
        pdf_uploads = PDFUpload.objects.all()

        # Prepare a list of dictionaries to return
        data = []
        for pdf in pdf_uploads:
            data.append({
                "id": pdf.id,
                "input_pdf": pdf.input_pdf.url if pdf.input_pdf else None,  # Assuming you are using FileField with url attribute
                "processed_pdf": pdf.processed_pdf.url if pdf.processed_pdf else None,
                "form_data_json": pdf.form_data_json.url if pdf.form_data_json else None,
                "normalized_data_json": pdf.normalized_data_json.url if pdf.normalized_data_json else None,
                "uploaded_at": pdf.uploaded_at
            })

        # Return the response with the prepared data as JSON
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)



# from django.shortcuts import render
# from .models import PDFUpload

# class PDFUploadListAPI(APIView):
#     """
#     API endpoint to retrieve all PDF uploads without using a serializer.
#     """
#     def get(self, request, *args, **kwargs):
#         # Fetch all records from the PDFUpload model
#         pdf_uploads = PDFUpload.objects.all()

#         # Prepare a list of dictionaries to return
#         data = []
#         for pdf in pdf_uploads:
#             data.append({
#                 "id": pdf.id,
#                 "input_pdf": pdf.input_pdf.url if pdf.input_pdf else None,
#                 "processed_pdf": pdf.processed_pdf.url if pdf.processed_pdf else None,
#                 "form_data_json": pdf.form_data_json.url if pdf.form_data_json else None,
#                 "normalized_data_json": pdf.normalized_data_json.url if pdf.normalized_data_json else None,
#                 "uploaded_at": pdf.uploaded_at
#             })

#         # Return the response with the prepared data to a template
#         return render(request, 'forms/upload.html', {'pdf_uploads': data})




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFUpload

class PDFGetProcessingAPI(APIView):

    def get(self, request, *args, **kwargs):
        """Handle the GET request to fetch the processed data by ID."""
        
        # Get the 'id' from the URL parameters (from kwargs)
        record_id = kwargs.get('id')

        # Check if the id is provided
        if not record_id:
            return Response({"status": "error", "message": "ID parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the record from the database
            pdf_upload = PDFUpload.objects.get(id=record_id)

            # Prepare the response with the stored data details
            result = {
                "status": "success",
                "message": "Data fetched successfully",
                "input_pdf": f"/media/{pdf_upload.input_pdf}",
                "file": f"/media/{pdf_upload.processed_pdf}",
                "form_data": f"/media/{pdf_upload.form_data_json}",
                "normalized_data": f"/media/{pdf_upload.normalized_data_json}",
                "database_entry_id": pdf_upload.id
            }

            return Response(result, status=status.HTTP_200_OK)

        except PDFUpload.DoesNotExist:
            return Response({"status": "success", "message": "Record not found."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": "success", "message": f"Error fetching record: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFUpload

class PDFProcessingDeleteAPI(APIView):

    def delete(self, request, *args, **kwargs):
        """Handle the DELETE request to remove a record by ID."""
        
        # Get the 'id' from the URL parameters (from kwargs)
        record_id = kwargs.get('id')

        # Check if the id is provided
        if not record_id:
            return Response({"status": "error", "message": "ID parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the record from the database
            pdf_upload = PDFUpload.objects.get(id=record_id)

            # Delete the record
            pdf_upload.delete()

            return Response({"status": "success", "message": "Record deleted successfully."},
                            status=status.HTTP_200_OK)

        except PDFUpload.DoesNotExist:
            return Response({"status": "success", "message": "Record not found."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": "success", "message": f"Error deleting record: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFUpload
from rest_framework.parsers import MultiPartParser, FormParser

class PDFProcessingSaveAPI(APIView):
    # Set up parsers for handling file uploads
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """Handle the POST request to save a PDFUpload record."""
        
        # Extract the files and other fields from the request
        input_pdf = request.FILES.get('input_pdf')
        processed_pdf = request.FILES.get('processed_pdf')
        form_data_json = request.FILES.get('form_data_json')
        normalized_data_json = request.FILES.get('normalized_data_json')

        # Validate required fields (input_pdf is mandatory)
        if not input_pdf:
            return Response({"status": "error", "message": "Input PDF is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a new PDFUpload record
            pdf_upload = PDFUpload.objects.create(
                input_pdf=input_pdf,
                processed_pdf=processed_pdf,
                form_data_json=form_data_json,
                normalized_data_json=normalized_data_json
            )

            # Prepare the response
            result = {
                "status": "success",
                "message": "Data saved successfully",
                "input_pdf": f"/media/{pdf_upload.input_pdf}",
                "file": f"/media/{pdf_upload.processed_pdf}",
                "form_data": f"/media/{pdf_upload.form_data_json}",
                "normalized_data": f"/media/{pdf_upload.normalized_data_json}",
                "database_entry_id": pdf_upload.id
            }

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": "error", "message": f"Error saving record: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFUpload
from rest_framework.parsers import JSONParser
import os
import json

class PDFUpdateProcessingAPI(APIView):
    parser_classes = [JSONParser]  # Use JSONParser for raw JSON input
    
    def put(self, request, *args, **kwargs):
        """Handle the PUT request to update the processed data by ID."""
        
        record_id = kwargs.get('id')

        # Check if the id is provided
        if not record_id:
            return Response({"status": "error", "message": "ID parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the record from the database
            pdf_upload = PDFUpload.objects.get(id=record_id)

            # Initialize response result
            result = {
                "status": "success",
                "message": "Data updated successfully",
                "database_entry_id": pdf_upload.id
            }

            # Update form_data_json if provided
            if 'form_data_json' in request.data:
                form_data = request.data['form_data_json']
                form_data_str = json.dumps(form_data)  # Convert dictionary to string
                form_data_path = f'form_data_{record_id}.json'
                
                # Write the JSON string to file
                with open(os.path.join('media', form_data_path), 'w') as f:
                    f.write(form_data_str)
                    
                pdf_upload.form_data_json = form_data_path
                result["form_data"] = f"/media/{pdf_upload.form_data_json}"

            # Update normalized_data_json if provided
            if 'normalized_data_json' in request.data:
                normalized_data = request.data['normalized_data_json']
                normalized_data_str = json.dumps(normalized_data)  # Convert dictionary to string
                normalized_data_path = f'normalized_data_{record_id}.json'
                
                # Write the JSON string to file
                with open(os.path.join('media', normalized_data_path), 'w') as f:
                    f.write(normalized_data_str)
                    
                pdf_upload.normalized_data_json = normalized_data_path
                result["normalized_data"] = f"/media/{pdf_upload.normalized_data_json}"

            # Save the changes to the database
            pdf_upload.save()

            return Response(result, status=status.HTTP_200_OK)

        except PDFUpload.DoesNotExist:
            return Response({"status": "error", "message": "Record not found."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": "error", "message": f"Error updating record: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
