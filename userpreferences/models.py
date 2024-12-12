from django.db import models
from authentication.models import CustomUser

# Default values as callables
def get_default_convertersion_types():
    return ['Giotto', '...']

class UserPreferences(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    conversion_type = models.JSONField(default=get_default_convertersion_types)

    def __str__(self):
        return f"{self.user.username}'s preferences"
