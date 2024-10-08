# Generated by Django 5.0.7 on 2024-08-18 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0006_userpreferences_accounts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='categories_expenses',
            field=models.JSONField(default=['Travel', 'Transfers', 'Supermarket', 'Income', 'Home', 'Health & Body & Mind', 'Rent', 'Gifts', 'Fun', 'Food Out', 'Dog', 'Clothes', 'Bills & Services']),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='categories_incomes',
            field=models.JSONField(default=['Salary', 'Sales']),
        ),
    ]