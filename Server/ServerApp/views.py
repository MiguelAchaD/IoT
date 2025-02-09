import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ServerApp.models import Patient, Api, Endpoint, ApiKeys, CustomUser, Reunion, History, Reunion, Record
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import datetime

@login_required
def dashboard(request, id=None):
    patient = Patient.objects.get(public_id=id)
    patient_ip = patient.ip

    client_api_name = "Clients"
    user_sensors = call_api(client_api_name, "get_sensor_results", extra_url_patient=f"http://{patient_ip}:5000")

    heart_rate = user_sensors.get("heartrate")
    ambient_temperature = user_sensors.get("temperature")
    #is_exposed_to_light = user_sensors.get("is_exposed_to_light")

    record = Record.objects.create(
        date_time=datetime.now(),
        heart_rate=heart_rate,
        ambient_temperature=ambient_temperature,
        is_exposed_to_light=0
    )

    today = datetime.today()
    print(today)
    history = History.objects.filter(patient=patient, day_of_record=today).first()

    if not history:
        history = History.objects.create(patient=patient, day_of_record=today)

    history.records.add(record)

    records = history.records.all()
    data = {
        "heart_rate": [record.heart_rate for record in records],
        "ambient_temperature": [record.ambient_temperature for record in records],
        "is_exposed_to_light": [str(record.is_exposed_to_light) for record in records],
        "timestamps": [record.date_time.strftime("%Y-%m-%d %H:%M:%S") for record in records],
    }

    weather_api_name = "Weather"
    weather_current_response = key_call_api(weather_api_name, "current", {"<CITY>": patient.city})
    weather_forecast_response = key_call_api(weather_api_name, "forecast", {"<CITY>": patient.city})
    weather_forecast_response['forecast'] = weather_forecast_response['forecast']['forecastday'][:5]

    dashboards = [
        {"type": "weather_current", "data": weather_current_response},
        {"type": "weather_forecast", "data": weather_forecast_response},
        {"type": "iot_data", "data": data},
    ]

    return render(request, "dashboard.html", {"patient": patient, "dashboards": dashboards, "data": data, "weather_current": weather_current_response, "weather_forecast": weather_forecast_response})


def home(request):
    return render(request, "home.html", {})


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

@login_required
def addPatient(request, ip, public_id, name, age, sex, city):
    patient, created = Patient.objects.get_or_create(
        public_id=public_id,
        defaults={
            'name': name,
            'ip': ip,
            'age': age,
            'sex': sex,
            'city': city,
            'status': 'INACTIVE',   
        }
    )

    request.user.patients.add(patient)

    return redirect("patients")

@login_required
def deletePatient(request, public_id):
    Patient.objects.filter(public_id=public_id).delete()
    return redirect("patients")

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
    else:
        return render(request, 'signin/register.html')

@login_required
def calendar(request, public_id):
    try:
        patient = Patient.objects.get(public_id=public_id)
        reunions = patient.reunions.all()

        request.session['patient_public_id'] = public_id

        return render(request, 'calendar.html', {'reunions': reunions})
    except Patient.DoesNotExist:
        return render(request, 'calendar.html', {'error': 'Patient not found'})


@login_required
def add_reunion(request, title, start, description, url):
    if request.method == 'POST':
        try:
            public_id = request.session.get('patient_public_id')
            if not public_id:
                return JsonResponse({'status': 'error', 'message': 'No patient selected'}, status=400)

            patient = Patient.objects.get(public_id=public_id)
            patient_ip = patient.ip

            reunion, created = Reunion.objects.get_or_create(
                title=title,
                description=description,
                url=url,
                start=start,
            )

            create_reunion_rp = call_api("Clients", "calendar_create", data={"title": f"{title}", "date_time": f"{start}", "url": f"{url}"}, extra_url_patient=f"http://{patient_ip}:5000")
            if create_reunion_rp.status_code not in [200, 300]:
                return JsonResponse({'status': 'error', 'message': f"{create_reunion_rp.content}"})

            patient.reunions.add(reunion)

            return JsonResponse({'status': 'success', 'created': created})
        except Patient.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Patient not found'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def update_reunion(request, title, start, description, url):
    if request.method == 'POST':
        public_id = request.session.get('patient_public_id')
        patient = Patient.objects.get(public_id=public_id)
        patient_ip = patient.ip
        reunion = Reunion.objects.get(title=title)
        if (reunion):
            reunion.title = title
            reunion.start = start
            reunion.description = description
            reunion.url = url
            update_reunion_rp = call_api("Clients", "calendar_modify", data={"title": f"{title}", "new_date_time": f"{start}", "new_url": f"{url}"}, extra_url_patient=f"http://{patient_ip}:5000")
            if update_reunion_rp.status_code not in [200, 300]:
                return JsonResponse({'status': 'error', 'message': f"{update_reunion_rp.content}"})
            reunion.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})

@login_required
def delete_reunion(request, title):
    if request.method == 'POST':
        public_id = request.session.get('patient_public_id')
        patient = Patient.objects.get(public_id=public_id)
        patient_ip = patient.ip
        reunion = get_object_or_404(Reunion, title=title)
        if (reunion):
            delete_reunion_rp = call_api("Clients", "calendar_remove", data={"title": f"{title}"}, extra_url_patient=f"http://{patient_ip}:5000")
            if delete_reunion_rp.status_code not in [200, 300]:
                return JsonResponse({'status': 'error', 'message': f"{delete_reunion_rp.content}"})
            reunion.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'})

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

def call_api(api_name, endpoint_name, parameters=None, data=None, extra_url_patient=None):
    try:
        api_object = Api.objects.get(name=api_name)
        endpoint_object = Endpoint.objects.get(name=endpoint_name)
    except:
        return None

    if extra_url_patient:
        api_object.base_url = extra_url_patient

    call_url = str(api_object.base_url) + str(endpoint_object.url)
    method = endpoint_object.method
    
    if (parameters):
        if (len(parameters.keys()) > 0):
            call_url = format_url(call_url, parameters)

    if (method == "GET"):
        return requests.get(url=call_url, headers=api_object.headers).json()
    elif (method == "POST"):
        return requests.post(url=call_url, json=data)

def format_url(call_url, parameters):
    for parameter in parameters.keys():
        call_url = call_url.replace(parameter, parameters.get(parameter))
    return call_url

def logout_view(request):
    logout(request)
    return redirect('login')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not (name and email and subject and message):
            return render(request, 'contact.html', {'error': 'All fields are required.'})

        try:
            send_mail(
                f'Contact Form Submission: {subject}',
                f'Message from {name} ({email}):\n\n{message}',
                'your_email@example.com',
                ['recipient_email@example.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully. Thank you!')
            return redirect('home')
        except Exception as e:
            return render(request, 'contact.html', {'error': f'Failed to send your message. Error: {e}'})
    else:
        return render(request, 'contact.html')
