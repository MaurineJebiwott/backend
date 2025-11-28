# contracts/models.py
from django.db import models
from django.conf import settings

class Contract(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("rejected", "Rejected"),
        ("partially_filled", "Partially Filled"),
        ("filled", "Filled")
    ]

    type = models.CharField(max_length=100)   # Treaty or Facultative
    cedant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="cedant_contracts",
        on_delete=models.CASCADE
    )
    # reinsurer = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     related_name="reinsurer_contracts",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )
    start_date = models.DateField()
    end_date = models.DateField()
    coverage = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 1,000,000
    total_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    allocated_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def remaining_percentage(self):
        return self.total_percentage - self.allocated_percentage

    def __str__(self):
        return f"{self.type} - {self.cedant.username}"
class ReinsurerParticipation(models.Model):
    STATUS_CHOICES = [
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    contract = models.ForeignKey(
        Contract, 
        on_delete=models.CASCADE, 
        related_name="participations"
    )
    reinsurer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participations"
    )
    percentage_taken = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="accepted")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reinsurer.username} - {self.percentage_taken}% - {self.status}"
