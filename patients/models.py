from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="patients/profiles/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "patients"

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def email(self):
        return self.user.email

    def get_age(self):
        if self.date_of_birth:
            from datetime import date

            today = date.today()
            return today.year - self.date_of_birth.year
        return None
