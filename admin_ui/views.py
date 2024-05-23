import requests

from django.views import View 
from django.shortcuts import render, redirect
from django.conf import settings


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return redirect('login_user')
        
        # Verify the token with a dedicated auth check endpoint, not logging related
        api_url = f'{settings.API_BASE_URL}/api/admin/check-token'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200 and 'message' in response.json():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login_user')


class DashboardView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        api_url = f'{settings.API_BASE_URL}/api/admin/dashboard'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Making the request to the Flask API to log the user action
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200 and 'message' in response.json():
            # If the logging was successful, render the dashboard
            return render(request, 'dashboard.html')
        else:
            # If logging failed, redirect to the login page
            return redirect('login_user')
