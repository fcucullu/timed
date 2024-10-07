from django.urls import path
from . import views

urlpatterns = [
    #Views
    path('convert/', views.convert, name='convert'),
        
]
