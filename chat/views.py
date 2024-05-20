import requests
import json

from django.views import View 
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from admin_ui.views import LoginRequiredMixin


class ChatUserListView(LoginRequiredMixin, View):
    def get(self, request):  
        api_url = f'{settings.API_BASE_URL}/api/admin/user/chats'
        access_token = request.COOKIES.get('access_token') 
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            print(users, "DFGHJ")
            return render(
                request, 
                'chat/chat.html',
                {
                    'chat_users': users
                }
            )
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
        

class UserAllChatView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        api_url = f'{settings.API_BASE_URL}/api/admin/response/{user_id}'
        access_token = request.COOKIES.get('access_token') 
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            message_content = response.json()
            return JsonResponse({'success': True, 'message_content': message_content})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')


class AdminResponseView(LoginRequiredMixin, View):
    def post(self, request):
        data = request.POST
        access_token = request.COOKIES.get('access_token')  
        if 'property_id'  in data:
            api_url = f'{settings.API_BASE_URL}/api/admin/property/response'
        else:
            api_url = f'{settings.API_BASE_URL}/api/admin/response'
        
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
            return JsonResponse({'error': "Something went wrong!"}), 400


class PropertyUserAllChatView(LoginRequiredMixin, View):
    def get(self, request, property_id, user_id):
        api_url = f'{settings.API_BASE_URL}/api/admin/property/response/{property_id}/{user_id}'
        access_token = request.COOKIES.get('access_token') 
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            message_content = response.json()
            return JsonResponse({'success': True, 'message_content': message_content})
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
        

class PropertyChatUsersListView(LoginRequiredMixin, View):
    def get(self, request):  
        api_url = f'{settings.API_BASE_URL}/api/admin/user/property/chat/list'
        access_token = request.COOKIES.get('access_token') 
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            users = response.json()
            return render(
                request, 
                'chat/property-chat.html',
                {
                    'property_users': users
                }
            )
        else:
            print(response.text)
            return render(request, 'pages/500error.html')
