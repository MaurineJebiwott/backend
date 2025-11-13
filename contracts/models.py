# contracts/models.py
from django.db import models
from django.conf import settings

class Contract(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("rejected", "Rejected"),
    ]

    type = models.CharField(max_length=100)   # Treaty or Facultative
    cedant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="cedant_contracts",
        on_delete=models.CASCADE
    )
    reinsurer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reinsurer_contracts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    coverage = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 1,000,000
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 40.0%

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.cedant.username}"
