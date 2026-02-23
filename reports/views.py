from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from patients.models import Patient
from .models import MedicalReport


@login_required
def my_reports(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)
    reports = patient.medical_reports.select_related('doctor').order_by('-report_date')
    return render(request, 'reports/my_reports.html', {'reports': reports})


@login_required
def download_report(request, pk):
    try:
        patient = request.user.patient_profile
        report = get_object_or_404(MedicalReport, pk=pk, patient=patient)
        return FileResponse(report.report_file.open(), as_attachment=True)
    except Patient.DoesNotExist:
        raise Http404
