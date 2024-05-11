import requests

from django.views import View 
from django.shortcuts import render, redirect
from django.conf import settings


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return redirect('login_user')
        
        api_url = f'{settings.API_BASE_URL}/api/admin/dashboard'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200 and 'message' in response.json():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login_user')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):     
        return render(request, 'dashboard.html')

