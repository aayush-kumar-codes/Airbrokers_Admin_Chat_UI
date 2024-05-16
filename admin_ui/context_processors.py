from django.views import View 
from django.shortcuts import render
import requests
import json

from django.views import View 
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse


def mqtt_connection_for_push_notification_context(request):
    api_url = f'{settings.API_BASE_URL}/api/admin/users'
    access_token = request.COOKIES.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(api_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        users = response.json()
    else:
        users = None

    property_api_url = f'{settings.API_BASE_URL}/api/user/properties'
    property_response = requests.get(property_api_url, headers=headers)

    if property_response.status_code == 200:
        properties = property_response.json()
        customer_service_properties = []
        if type(properties) == dict:
            properties= None
        elif type(properties) == list:
            for property in properties:
                if property['owner_info']['name'] == 'Customer-Service':
                    customer_service_properties.append(property)
    else:
        properties = None
    
    mqtt_websocket_url = settings.MQTT_WEBSOCKET_URL
    mqtt_username = settings.MQTT_BROKER_USERNAME
    mqtt_passwd = settings.MQTT_BROKER_PASSWD
    api_url = settings.API_BASE_URL
     
    return {
        'properties': customer_service_properties,
        'users': users,
        'API_URL': api_url,
        'MQTT_WEBSOCKET_URL':mqtt_websocket_url,
        'MQTT_USERNAME': mqtt_username,
        'MQTT_PASSWD': mqtt_passwd
    }
