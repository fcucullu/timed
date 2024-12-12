from django.http import HttpResponse    
from ...utils.giotto.giotto_converter import Giotto
from datetime import datetime

class AbstractConverter:
    def __init__(self, uploaded_file, conversion_type):
        """
        Initialize the converter with the necessary parameters.
        
        Parameters:
        - uploaded_file: The file uploaded by the user (data for conversion).
        - conversion_type: A string identifying the type of converter to use.
        - mapping_file: Optional mapping file for converters that need it.
        """
        self.uploaded_file = uploaded_file
        self.conversion_type = conversion_type.lower()
        self.converters_map = {
            'giotto': Giotto,
            'team_system': 'TeamSystem',
            'randazzo': 'Randazzo',
        }

    def convert(self):
        """
        Handle the conversion process based on the selected conversion type.
        
        returns: HttpResponse containing the converted file for download.
        """
        # Check if the conversion type is supported
        if self.conversion_type not in self.converters_map:
            raise ValueError(f"Unsupported conversion type: {self.conversion_type}")
        
        # Instantiate the appropriate converter class
        converter_class = self.converters_map[self.conversion_type]()

        try:
            # Call the common method to handle the conversion
            converted_file = converter_class.convert_data(self.uploaded_file)
            if not converted_file:
                raise ValueError("Conversion failed: No data returned.")

        except Exception as e:
            raise ValueError(f"An error occurred during conversion: {e}")

        # Generate a formatted timestamped file name
        now = datetime.now()
        formatted_date = now.strftime("%Y%m%d_%H%M%S")
        output_filename = f"giotto_output_{formatted_date}.csv"

        # After conversion, return the file as a downloadable response
        response = HttpResponse(converted_file, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={output_filename}'
        return response