from django.views import View 
from django.shortcuts import render


class DashboardView(View):
    def get(self, request):       
        return render(request, 'dashboard.html')


class Homeview(View):
    def get(self, request):       
        return render(request, 'users/login.html')
