from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="doctors/profiles/", null=True, blank=True
    )
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    available_days = models.CharField(max_length=200, blank=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "doctors"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return "Dr. {} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return "Dr. {} {}".format(self.first_name, self.last_name)
