import requests
from django.views import View 
from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings


class DashboardView(View):
    def get(self, request):       
        return render(request, 'dashboard.html')
    

class AllDocumentsView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/documents'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            documents = response.json()
            return render(request, 'documents.html', {'templates':documents})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   


class UpdateDocumentView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/document/update'

        data = {
            'docname': request.POST.get('docname', ''),
            'description': request.POST.get('description', ''),
            'rename': request.POST.get('rename', '')
        }

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.put(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            print(message)
            return JsonResponse({'success': True})
        else:
            if response.status_code== 400:
                return JsonResponse({'error': response.json().get('error')})
            return JsonResponse({'error': "Something went wrong!"}) 
            
       
    

class DocumentsView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/templates'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            folder_structure = response.json()
            return render(request, 'templates.html', {'folder_structure':folder_structure})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   
