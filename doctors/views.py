from django.shortcuts import render, get_object_or_404
from .models import Doctor, Department


def doctor_list(request):
    specialty = request.GET.get("specialty", "")
    doctors = Doctor.objects.filter(is_active=True).select_related("department")
    if specialty:
        doctors = doctors.filter(specialization__icontains=specialty)
    departments = Department.objects.all()
    return render(
        request,
        "doctors/doctor_list.html",
        {
            "doctors": doctors,
            "departments": departments,
            "selected_specialty": specialty,
        },
    )


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    return render(request, "doctors/doctor_detail.html", {"doctor": doctor})
