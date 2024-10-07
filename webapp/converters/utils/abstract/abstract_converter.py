from django.http import HttpResponse
import os
from ...utils.giotto.giotto_converter import Giotto

class AbstractConverter:
    def __init__(self, uploaded_file, conversion_type, mapping_file=None):
        """
        Initialize the converter with the necessary parameters.
        
        Parameters:
        - uploaded_file: The file uploaded by the user (data for conversion).
        - conversion_type: A string identifying the type of converter to use.
        - mapping_file: Optional mapping file for converters that need it.
        """
        self.uploaded_file = uploaded_file
        self.conversion_type = conversion_type.lower()
        self.mapping_file = mapping_file
        self.converters_map = {
            'giotto': Giotto,
            'team_system': TeamSystem,
            'randazzo': Randazzo,
        }

    def convert(self):
        """
        Handle the conversion process based on the selected conversion type.
        
        return: A response or result from the conversion process.
        """
        # Check if the conversion type is supported
        if self.conversion_type not in self.converters_map:
            raise ValueError(f"Unsupported conversion type: {self.conversion_type}")

        # Instantiate the appropriate converter class
        converter_class = self.converters_map[self.conversion_type]()
        
        # Call the common method to handle the conversion
        converted_file_path = converter_class.convert_data(self.uploaded_file, self.mapping_file)

        # After conversion, return the file as a downloadable response
        if os.path.exists(converted_file_path):
            with open(converted_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(converted_file_path)}'
                return response
        else:
            return HttpResponse("Error: Converted file not found.", status=404)
