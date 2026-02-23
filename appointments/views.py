from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient


def book_appointment(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('first_name')
    doctor_id = request.GET.get('doctor')
    selected_doctor = None
    if doctor_id:
        try:
            selected_doctor = Doctor.objects.get(pk=doctor_id, is_active=True)
        except Doctor.DoesNotExist:
            pass

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to book an appointment.')
            return redirect('/patients/login/?next=/appointments/book/')

        try:
            patient = request.user.patient_profile
        except Patient.DoesNotExist:
            patient = Patient.objects.create(user=request.user)

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        appointment_type = request.POST.get('appointment_type', 'in_person')
        reason = request.POST.get('reason', '')
        symptoms = request.POST.get('symptoms', '')

        try:
            doctor = Doctor.objects.get(pk=doctor_id, is_active=True)
            existing = Appointment.objects.filter(
                doctor=doctor, appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            )
            if existing.exists():
                messages.error(request, 'This time slot is already booked. Please choose another.')
            else:
                appt = Appointment.objects.create(
                    patient=patient, doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    appointment_type=appointment_type,
                    reason=reason, symptoms=symptoms
                )
                messages.success(request, 'Appointment booked! Your appointment ID is #{}.'.format(appt.id))
                return redirect('patient_dashboard')
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor not found.')

    return render(request, 'appointments/book.html', {
        'doctors': doctors,
        'selected_doctor': selected_doctor,
    })


@login_required
def my_appointments(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)
    appointments = patient.appointments.select_related('doctor').order_by('-appointment_date')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def cancel_appointment(request, pk):
    try:
        patient = request.user.patient_profile
        appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
        if appointment.status in ['pending', 'confirmed']:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'This appointment cannot be cancelled.')
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found.')
    return redirect('my_appointments')
