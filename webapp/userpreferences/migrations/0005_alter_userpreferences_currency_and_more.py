# Generated by Django 5.0.7 on 2024-08-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0004_alter_userpreferences_rows_per_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='currency',
            field=models.CharField(default='EUR - Euro'),
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='currency_code',
            field=models.CharField(default='EUR'),
        ),
    ]