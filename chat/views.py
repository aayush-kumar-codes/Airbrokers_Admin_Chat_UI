import requests
import json

from django.views import View 
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from admin_ui.views import LoginRequiredMixin


class ChatView(LoginRequiredMixin, View):
    def get(self, request):  
        api_url = f'{settings.API_BASE_URL}/api/admin/user/chats'
        access_token = request.COOKIES.get('access_token') 
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            mqtt_websocket_url = settings.MQTT_WEBSOCKET_URL
            mqtt_username = settings.MQTT_BROKER_USERNAME
            mqtt_passwd = settings.MQTT_BROKER_PASSWD
            api_url = settings.API_BASE_URL
            return render(
                request, 
                'chat/chat.html',
                {
                    'users': users, 
                    'MQTT_WEBSOCKET_URL':mqtt_websocket_url,
                    'MQTT_USERNAME': mqtt_username,
                    'MQTT_PASSWD': mqtt_passwd,
                    'API_URL': api_url
                }
            )
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
        

class UpdateChatStatusView(LoginRequiredMixin, View):
    def post(self, request):
        api_url = f'{settings.API_BASE_URL}/api/admin/user/chat-status'
        access_token = request.COOKIES.get('access_token')  

        headers = {'Authorization': f'Bearer {access_token}'}

        data = json.loads(request.body)
        email = data.get('email')

        response = requests.post(api_url, headers=headers, json={'email':email})

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "Something went wrong!"})


class AdminResponseView(LoginRequiredMixin, View):
    def post(self, request):
        api_url = f'{settings.API_BASE_URL}/api/admin/response'
        access_token = request.COOKIES.get('access_token')  

        headers = {'Authorization': f'Bearer {access_token}'}

        data = request.POST
        media_file = request.FILES.get('media_file')
        files = {}
        if media_file:
            files = {'media_file': media_file}
        
        response = requests.post(api_url, headers=headers, data=data, files=files)

        if response.status_code == 200:
            message = response.json()
            return JsonResponse({'success': True})
        else:
            print(response.text)
            return JsonResponse({'error': "Something went wrong!"})
