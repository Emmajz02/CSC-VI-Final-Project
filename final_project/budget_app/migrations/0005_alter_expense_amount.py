# Generated by Django 5.1.6 on 2025-04-06 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_app', '0004_remove_expense_date_remove_expense_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
