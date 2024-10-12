from django.db import models
from authentication.models import CustomUser

class ConversionHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    company = models.CharField(max_length=255) 
    date = models.DateTimeField(auto_now_add=True) 
    conversion_used = models.CharField(max_length=255) 
    status = models.CharField(max_length=50)  # Final status of the conversion

    def __str__(self):
        return f'{self.user.username} - {self.conversion_used} - {self.status}'
