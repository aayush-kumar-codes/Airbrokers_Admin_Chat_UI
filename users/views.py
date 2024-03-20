import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View 
from django.shortcuts import render

from django.conf import settings



class ListView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/users'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            return render(request, 'users/userlist.html',{'users': users})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')


class AddView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/user/register'
        data = {
            'uuid': request.POST.get('uuid', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'facebook': request.POST.get('facebook', ''),
            'gmail': request.POST.get('gmail', ''),
            'linkedin': request.POST.get('linkedin', ''),
            'password': request.POST.get('password', '')
        }

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': response.json().get('error')})


class UpdateView(View):
    def post(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/user/update'

        data = {
            'email': request.POST.get('username', ''),
            'first_name': request.POST.get('upfirst_name', ''),
            'last_name': request.POST.get('uplast_name', ''),
            'phone': request.POST.get('upphone', ''),
            'facebook': request.POST.get('upfacebook', ''),
            'gmail': request.POST.get('upgmail', ''),
            'linkedin': request.POST.get('uplinkedin', ''),
            'password': request.POST.get('uppassword', '')
        }

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        files = {}
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            files['profile_pic'] = profile_pic
        
        response = requests.put(api_url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            message = response.json()
            print(message)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "Something went wrong!"})


class DeleteView(View):
    def post(self, request):
        api_url = 'http://155.138.160.153:5099/api/admin/user/delete'

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        data = json.loads(request.body)
        email = data.get('email')

        response = requests.delete(api_url, headers=headers, json={'email':email})

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "Something went wrong!"})


class MediaView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/user/media'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            allmedia = response.json()
            return render(request, 'users/media.html', {'allmedia':allmedia})
        else:
            print(response.text)
            return render(request, 'pages/500error.html') 
    

class DownloadedDocsView(View):
    def get(self, request): 
        api_url = 'http://155.138.160.153:5099/api/admin/users'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            return render(request, 'users/downloaded_docs.html',{'users': users})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
    

class UploadedDocsView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/user/uploaded-docs'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            uploaded_docs = response.json()
            return render(request, 'users/uploaded_docs.html', {'uploaded_docs':uploaded_docs})
        else:
            print(response.text)
            return render(request, 'pages/500error.html') 

