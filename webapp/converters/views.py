from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import Converter
from .utils.abstract.abstract_converter import AbstractConverter
from django.http import HttpResponse



@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def convert(request):
    if request.method == 'GET':
        return render(request, 'converters/convert.html')

    if request.method == 'POST':
        uploaded_file = request.FILES.get('uploaded_file')
        conversion_type = request.POST.get('conversion_type')

        context = {
            'conversion_type': conversion_type,
        }

        if not conversion_type or conversion_type == 'Select an option':
            messages.error(request, 'Select a converter')
            return render(request, 'converters/convert.html', context)

        if not uploaded_file:
            messages.error(request, 'Select a file to convert')
            return render(request, 'converters/convert.html', context)

        try:
            # Call the abstract converter to handle the file conversion
            converter = AbstractConverter(uploaded_file, conversion_type)
            response = converter.convert()
            if not isinstance(response, HttpResponse):
                raise ValueError("Conversion failed: the response is empty. Check your file and try again.")
            
            messages.success(request, 'Conversion successful! Your file should be automatically downloaded.')
            
            # Save conversion details to the database
            Converter.objects.create(
                user=request.user,
                conversion_used=conversion_type,
                status='Success'
            )

            return response  
        
        except Exception as e:
            messages.error(request, 'An error occurred during conversion. Please check the file and try again.')
            
            # Save conversion details with failure status
            Converter.objects.create(
                user=request.user,
                conversion_used=conversion_type,
                status='Failure'
            )
            return render(request, 'converters/convert.html', context)
