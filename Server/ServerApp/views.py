from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from ServerApp.models import Patient, Api, Endpoint, ApiKeys, CustomUser
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .models import Reunion
from .forms import ReunionForm

@login_required
def dashboard(request, id=None):
    patient = Patient.objects.get(public_id=id)
    history = patient.record_history

    print(f"{patient=}")
    print(f"{patient.public_id=}")
    print(f"{patient.city=}")

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

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('password')
        new_password_validation = request.POST.get('password-validation')

        if username and username != user.username:
            if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                return render(request, "profile.html", {"user": user, "error": "The username is already in use"})
        
        if email and email != user.email:
            if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                return render(request, "profile.html", {"user": user, "error": "The email is already in use"})

        if new_password or new_password_validation:
            if not old_password:
                return render(request, "profile.html", {"user": user, "error": "Insert the old password to validate your identity"})
            
            if not user.check_password(old_password):
                return render(request, "profile.html", {"user": user, "error": "Wrong old password"})

            if new_password != new_password_validation:
                return render(request, "profile.html", {"user": user, "error": "The passwords don't coincide"})

            if new_password == old_password:
                return render(request, "profile.html", {"user": user, "error": "The passwords are the same"})

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.username = username or user.username
        user.email = email or user.email
        user.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return render(request, "profile.html", {"user": user})

    return render(request, "profile.html", {"user": user})



@login_required
def patients(request):
    patients = request.user.patients.all()

    rows_per_page = 10
    paginator = Paginator(patients, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = rows_per_page - len(page_obj)

    return render(request, 'patients.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows),
    })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            return render(request, 'signin/login.html', {'error': 'Invalid credentials'})
    return render(request, 'signin/login.html')

def register(request):
    if request.method == 'POST':
        continue_process = True
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            continue_process = False
            error = 'Passwords do not match.'

        if continue_process and CustomUser.objects.filter(email=email).exists():
            continue_process = False
            error = 'Email is already registered.'

        if continue_process:
            CustomUser.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
        else:
            return render(request, 'signin/register.html', {'error': error})

    return render(request, 'signin/register.html')

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

def lista_reuniones(request):
    reuniones = Reunion.objects.all()
    return render(request, 'lista_reuniones.html', {'reuniones': reuniones})

def nueva_reunion(request):
    if request.method == 'POST':
        form = ReunionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reuniones')
    else:
        form = ReunionForm()
    return render(request, 'nueva_reunion.html', {'form': form})