from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    period = models.CharField(max_length=50, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])

    def __str__(self):
        return f"{self.user.username}'s Budget: ${self.amount} ({self.period})"