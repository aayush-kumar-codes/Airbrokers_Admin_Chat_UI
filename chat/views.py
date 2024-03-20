import requests
import json

from django.views import View 
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

class ChatView(View):
    def get(self, request):  
        api_url = 'http://155.138.160.153:5099/api/admin/user/chats'
        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            return render(request, 'chat/chat.html',{'users': users})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
        

class UpdateChatStatusView(View):
    def post(self, request):
        api_url = 'http://155.138.160.153:5099/api/admin/user/chat-status'

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        data = json.loads(request.body)
        email = data.get('email')

        response = requests.post(api_url, headers=headers, json={'email':email})

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "Something went wrong!"})


class AdminResponseView(View):
    def post(self, request):
        api_url = 'http://155.138.160.153:5099/api/admin/response'

        headers = {'Authorization': f'Bearer {settings.API_KEY}'}

        data = json.loads(request.body)

        response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            message = response.json()
            print(message)
            return JsonResponse({'success': True})
        else:
            print(response.text)
            return JsonResponse({'error': "Something went wrong!"})
