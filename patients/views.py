from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Patient


def register(request):
    if request.user.is_authenticated:
        return redirect("patient_dashboard")
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        phone = request.POST.get("phone", "")
        gender = request.POST.get("gender", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            patient = Patient.objects.create(user=user, phone=phone, gender=gender)  # noqa: F841
            login(request, user)
            messages.success(
                request, "Welcome! Your account has been created successfully."
            )
            return redirect("patient_dashboard")
    return render(request, "patients/register.html")


def patient_login(request):
    if request.user.is_authenticated:
        return redirect("patient_dashboard")
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(
                request, "Welcome back, {}!".format(user.first_name or user.username)
            )
            next_url = request.GET.get("next", "patient_dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    return render(request, "patients/login.html")


def patient_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")


@login_required
def dashboard(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)

    appointments = patient.appointments.select_related("doctor").order_by(
        "-appointment_date"
    )[:5]
    reports = patient.medical_reports.order_by("-report_date")[:5]
    return render(
        request,
        "patients/dashboard.html",
        {
            "patient": patient,
            "appointments": appointments,
            "reports": reports,
            "total_appointments": patient.appointments.count(),
            "pending_appointments": patient.appointments.filter(
                status="pending"
            ).count(),
            "total_reports": patient.medical_reports.count(),
        },
    )


@login_required
def profile(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)

    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()
        patient.phone = request.POST.get("phone", patient.phone)
        patient.gender = request.POST.get("gender", patient.gender)
        patient.address = request.POST.get("address", patient.address)
        patient.blood_group = request.POST.get("blood_group", patient.blood_group)
        patient.emergency_contact_name = request.POST.get("emergency_contact_name", "")
        patient.emergency_contact_phone = request.POST.get(
            "emergency_contact_phone", ""
        )
        patient.allergies = request.POST.get("allergies", "")
        patient.medical_history = request.POST.get("medical_history", "")
        dob = request.POST.get("date_of_birth", "")
        if dob:
            patient.date_of_birth = dob
        if "profile_image" in request.FILES:
            patient.profile_image = request.FILES["profile_image"]
        patient.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("patient_profile")
    return render(request, "patients/profile.html", {"patient": patient})
