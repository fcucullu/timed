from django.db import models
from django.contrib.auth.models import User

class Converter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True) 
    conversion_used = models.CharField(max_length=255) 
    status = models.CharField(max_length=50)  # Final status of the conversion

    def __str__(self):
        return f'{self.user.username} - {self.conversion_used} - {self.status}'
