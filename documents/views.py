import requests
from django.views import View 
from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings
from admin_ui.views import LoginRequiredMixin


class AllDocumentsView(LoginRequiredMixin, View):
    def get(self, request):  
        api_url = f'{settings.API_BASE_URL}/api/admin/documents'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            documents = response.json()
            api_base_url = settings.API_BASE_URL
            return render(request, 'documents/documents.html', {'templates':documents, 'BASE_URL': api_base_url})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   


class UpdateDocumentView(LoginRequiredMixin, View):
    def post(self, request): 
        api_url = f'{settings.API_BASE_URL}/api/admin/document/update'
        access_token = request.COOKIES.get('access_token')  

        data = {
            'docname': request.POST.get('docname', ''),
            'description': request.POST.get('description', ''),
            'rename': request.POST.get('rename', ''),
            'folder': request.POST.get('doctype', '')
        }

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.put(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success':  True})
        else:
            if response.status_code== 400:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 


class FlFormsView(LoginRequiredMixin, View):
    def get(self, request):
        api_url = f'{settings.API_BASE_URL}/api/admin/flforms'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            folders_and_files = response.json()
            return render(request, 'documents/flforms.html', {'folders_and_files':folders_and_files})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   


class MnFormsView(LoginRequiredMixin, View):
    def get(self, request):
        api_url = f'{settings.API_BASE_URL}/api/admin/mnforms'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            folders_and_files = response.json()
            return render(request, 'documents/mnforms.html', {'folders_and_files':folders_and_files})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class SingleFlFormsView(LoginRequiredMixin, View):
    def get(self, request, filename, folder):
        api_url = f'{settings.API_BASE_URL}/api/admin/flforms/{filename}/{folder}'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            file = response.json()
            api_base_url = settings.API_BASE_URL
            return render(request, 'documents/single_flforms.html', {'file': file, 'BASE_URL': api_base_url})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class SingleMnFormsView(LoginRequiredMixin, View):
    def get(self, request, filename, folder):
        api_url = f'{settings.API_BASE_URL}/api/admin/mnforms/{filename}/{folder}'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            file = response.json()
            api_base_url = settings.API_BASE_URL
            return render(request, 'documents/single_mnforms.html', {'file': file, 'BASE_URL': api_base_url})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')  


class UploadDocumentView(LoginRequiredMixin, View):
    def post(self, request): 
        api_url = f'{settings.API_BASE_URL}/api/admin/document/upload'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}

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
            return JsonResponse({'success': True})
        else:
            if response.status_code== 400:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 


class MoveFlFormsDocumentView(LoginRequiredMixin, View):
    def post(self, request): 
        api_url = f'{settings.API_BASE_URL}/api/admin/document/flforms/move'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}

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
        

class MoveMnFormsDocumentView(LoginRequiredMixin, View):
    def post(self, request): 
        api_url = f'{settings.API_BASE_URL}/api/admin/document/mnforms/move'
        access_token = request.COOKIES.get('access_token')  
        headers = {'Authorization': f'Bearer {access_token}'}

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


class SingleFormQuestionAddView(LoginRequiredMixin, View):
    def post(self, request):
        access_token = request.COOKIES.get('access_token') 
        api_url = f'{settings.API_BASE_URL}/api/admin/forms/question' 
        headers = {'Authorization': f'Bearer {access_token}'}

        data  = {
            "question" : request.POST.getlist('question'),
            "type" : request.POST.get('type'),
            "folder": request.POST.get('folder'),
            "url" : request.POST.get('url'),
            "name": request.POST.get('name')
        }
        response = requests.post(api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            print(response.text)
            return JsonResponse({'error': "Something went wrong!"}) 
