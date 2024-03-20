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
        api_url = 'http://155.138.160.153:5099/api/admin/templates'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            documents = response.json()
            return render(request, 'documents.html', {'templates':documents})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')   
        