from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    period = models.CharField(max_length=50, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])
    profile_picture_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Budget: ${self.amount} ({self.period})"
    
class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category}: -${self.amount}"
    