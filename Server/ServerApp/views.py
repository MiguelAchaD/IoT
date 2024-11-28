from django.shortcuts import render
from django.core.paginator import Paginator
from ServerApp.models import Patient

def dashboard(request, id=None):
    patient = Patient.objects.get(public_id=id)
    return render(request, "dashboard.html", {"patient": patient})

def home(request):
    return render(request, "home.html", {})

def profile(request):
    return render(request, "profile.html", {})

from django.core.paginator import Paginator
from django.shortcuts import render

def patients(request):
    patients = Patient.objects.all()

    print(patients)

    rows_per_page = 10
    paginator = Paginator(patients, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = rows_per_page - len(page_obj)

    return render(request, 'patients.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows),
    })
