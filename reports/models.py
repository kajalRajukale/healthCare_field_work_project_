from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class MedicalReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ("lab", "Lab Test"),
        ("radiology", "Radiology"),
        ("prescription", "Prescription"),
        ("discharge", "Discharge Summary"),
        ("referral", "Referral Letter"),
        ("other", "Other"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="medical_reports"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_reports",
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_file = models.FileField(upload_to="reports/%Y/%m/")
    report_date = models.DateField()
    is_confidential = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medical_reports"
        ordering = ["-report_date"]

    def __str__(self):
        return "{} - {}".format(self.title, self.patient)
