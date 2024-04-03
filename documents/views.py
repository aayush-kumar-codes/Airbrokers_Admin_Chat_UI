import requests
from django.views import View 
from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings


class AllDocumentsView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/documents'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            documents = response.json()
            return render(request, 'documents/documents.html', {'templates':documents})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   


class UpdateDocumentView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/document/update'

        data = {
            'docname': request.POST.get('docname', ''),
            'description': request.POST.get('description', ''),
            'rename': request.POST.get('rename', ''),
            'folder': request.POST.get('doctype', '')
        }

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.put(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success':  True})
        else:
            if response.status_code== 400:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 


class FlFormsView(View):
    def get(self, request):
        api_url = 'http://155.138.160.153:5099/api/admin/flforms'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            folders_and_files = response.json()
            return render(request, 'documents/flforms.html', {'folders_and_files':folders_and_files})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   


class MnFormsView(View):
    def get(self, request):
        api_url = 'http://155.138.160.153:5099/api/admin/mnforms'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            folders_and_files = response.json()
            return render(request, 'documents/mnforms.html', {'folders_and_files':folders_and_files})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class SingleFlFormsView(View):
    def get(self, request, filename, folder):
        api_url = f'http://155.138.160.153:5099/api/admin/flforms/{filename}/{folder}'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            file = response.json()
            return render(request, 'documents/single_flforms.html', {'file': file})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class SingleMnFormsView(View):
    def get(self, request, filename, folder):
        api_url = f'http://155.138.160.153:5099/api/admin/mnforms/{filename}/{folder}'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            file = response.json()
            return render(request, 'documents/single_mnforms.html', {'file': file})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class UploadDocumentView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/document/upload'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        file = request.FILES.get('file')
        folder = request.POST.get('folder')
        new_folder = request.POST.get('new_folder')
        folder_type = request.POST.get('folder_type')

        if not file or not(folder or new_folder):
            return JsonResponse({'error': "All fields are required!"})
        
        if folder and new_folder:
            return JsonResponse({'error': "Please provide a single folder only!"})
        
        if file.content_type != 'application/pdf':
            return JsonResponse({'error': "Only PDF files are allowed!"})
        
        files = {'file': file}
        data = {'folder': folder, 'folder_type': folder_type}

        if new_folder:
            data['new_folder'] = new_folder

        response = requests.post(api_url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            message = response.json()
            print(message)
            return JsonResponse({'success': True})
        else:
            if response.status_code== 400:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 


class MoveFlFormsDocumentView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/document/flforms/move'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        filename= request.POST.get('filename')
        source_folder = request.POST.get('source_folder')
        dest_folder = request.POST.get('dest_folder')

        if not dest_folder or not filename:
            return JsonResponse({'error': "All fields are required!"})

        data = {
            'filename': filename,
            'source_folder': source_folder, 
            'dest_folder': dest_folder
        }

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            if response.status_code== 404:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 
        

class MoveMnFormsDocumentView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/document/mnforms/move'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        filename= request.POST.get('filename')
        source_folder = request.POST.get('source_folder')
        dest_folder = request.POST.get('dest_folder')

        if not dest_folder or not filename:
            return JsonResponse({'error': "All fields are required!"})

        data = {
            'filename': filename,
            'source_folder': source_folder, 
            'dest_folder': dest_folder
        }
        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            if response.status_code== 404:
                return JsonResponse({'error': response.json().get('error')})
            print(response.text)
            return JsonResponse({'error': "Something went wrong!"}) 
