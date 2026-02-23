from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    from doctors.models import Doctor
    from blog.models import BlogPost
    featured_doctors = Doctor.objects.filter(is_active=True)[:6]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'hospital/home.html', {
        'featured_doctors': featured_doctors,
        'recent_posts': recent_posts,
    })


def about(request):
    from doctors.models import Doctor
    doctors_count = Doctor.objects.filter(is_active=True).count()
    return render(request, 'hospital/about.html', {'doctors_count': doctors_count})


def services(request):
    services_list = [
        {'icon': '🫀', 'name': 'Cardiology', 'desc': 'Advanced heart care and cardiac surgery services.'},
        {'icon': '🧠', 'name': 'Neurology', 'desc': 'Comprehensive brain and nervous system treatment.'},
        {'icon': '🦴', 'name': 'Orthopedics', 'desc': 'Bone, joint, and musculoskeletal care.'},
        {'icon': '👁️', 'name': 'Ophthalmology', 'desc': 'Complete eye care and vision correction.'},
        {'icon': '🦷', 'name': 'Dental Care', 'desc': 'Full-service dental and oral health treatments.'},
        {'icon': '🤰', 'name': 'Gynecology', 'desc': "Women's health and maternity services."},
        {'icon': '🧬', 'name': 'Oncology', 'desc': 'Cancer diagnosis, treatment and support.'},
        {'icon': '🩺', 'name': 'General Medicine', 'desc': 'Primary care and preventive health services.'},
        {'icon': '🩻', 'name': 'Radiology', 'desc': 'Medical imaging, X-ray, MRI and CT scans.'},
        {'icon': '🧪', 'name': 'Pathology', 'desc': 'Advanced diagnostic laboratory services.'},
        {'icon': '💊', 'name': 'Pharmacy', 'desc': '24/7 in-house pharmacy with all medicines.'},
        {'icon': '🚑', 'name': 'Emergency Care', 'desc': 'Round-the-clock emergency and trauma care.'},
    ]
    return render(request, 'hospital/services.html', {'services': services_list})


def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Your message has been sent successfully! We will contact you soon.')
        return redirect('contact')
    return render(request, 'hospital/contact.html')
