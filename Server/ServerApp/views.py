from django.shortcuts import render
from django.core.paginator import Paginator
from ServerApp.models import Patient, Api, Endpoint, ApiKeys, Key
import requests

def dashboard(request, id=None):
    patient = Patient.objects.get(public_id=id)
    history = patient.record_history

    weather_api_name = "Weather"
    weather_current_response = key_call_api(weather_api_name, "current", {"<CITY>": patient.city})
    weather_forecast_response = key_call_api(weather_api_name, "forecast", {"<CITY>": patient.city})
    weather_forecast_response['forecast'] = weather_forecast_response['forecast']['forecastday'][:5]

    dashboards = [
        {"type": "weather_current", "data": weather_current_response},
        {"type": "weather_forecast", "data": weather_forecast_response},
    ]

    return render(request, "dashboard.html", {"patient": patient, "dashboards": dashboards})


def home(request):
    return render(request, "home.html", {})

def profile(request):
    return render(request, "profile.html", {})

def patients(request):
    patients = Patient.objects.all()

    rows_per_page = 10
    paginator = Paginator(patients, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = rows_per_page - len(page_obj)

    return render(request, 'patients.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows),
    })

## EXTRA FUNCTIONS

def key_call_api(api_name, endpoint_name, parameters=None):
    try:
        api_keys = ApiKeys.objects.get(api_name=api_name)
        key = api_keys.get_random_key()
    except ApiKeys.DoesNotExist:
        key = None

    if key:
        parameters["<KEY>"] = key
        weather_api_result = call_api(api_name, endpoint_name, parameters)
        return weather_api_result
    else:
        return None

def call_api(api_name, endpoint_name, parameters=None):
    try:
        api_object = Api.objects.get(name=api_name)
        endpoint_object = Endpoint.objects.get(name=endpoint_name)
    except:
        return None
    
    call_url = str(api_object.base_url) + str(endpoint_object.url)
    method = endpoint_object.method
    
    if (len(parameters.keys()) > 0):
        call_url = format_url(call_url, parameters)

    if (method == "GET"):
        return requests.get(url=call_url, headers=api_object.headers).json()
    elif (method == "POST"):
        return requests.post(url=call_url)

def format_url(call_url, parameters):
    for parameter in parameters.keys():
        call_url = call_url.replace(parameter, parameters.get(parameter))
    return call_url