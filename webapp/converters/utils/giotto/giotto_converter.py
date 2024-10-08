import pandas as pd
import os
import json
from datetime import datetime, timedelta
import io

class Giotto:
    def __init__(self):
        self.shift_type_mapping = self.load_shift_type_mapping()
    
    def load_shift_type_mapping(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'shift_type_mapping.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                shift_type_mapping = json.load(f)
            return shift_type_mapping
        except Exception as e:
            print(f"Error loading JSON mapping file: {e}")
            return {}
        
    def read_file(self, uploaded_file):
        data = pd.read_csv(uploaded_file).values.tolist()
        return data

    def format_duration_to_hhcc(self, duration, date_range_length):
        duration_per_day = duration / date_range_length
        hours = int(duration_per_day)
        minutes = int((duration_per_day - hours) * 100)
        return f"{hours:02}{minutes:02}"

    def format_date(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y%m%d')

    def generate_date_range(self, start_date, end_date, shift_type_account_weekend):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        date_range = [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]

        if not shift_type_account_weekend:
            # Filter out weekends if weekends should not be counted
            date_range = [date for date in date_range 
                        if (start + timedelta(days=int(date) - int(date_range[0]))).weekday() < 5]
        return date_range

    def convert_format_to_giotto(self, data):
        data = self.read_file(data)
        giotto_lines = []
        
        for row in data:
            company_id = row[1]  
            worker_id = row[2]  
            start_date = row[3]  
            end_date = row[4]  
            shift_type = row[5]  
            duration_type = '2'  
            try:
                shift_type_info = self.shift_type_mapping.get(shift_type)
                if not shift_type_info:
                    raise ValueError(f"Shift type {shift_type} not found in mapping.")
                shift_type_code = shift_type_info[0]
                shift_type_account_weekend = shift_type_info[1]
            except Exception as e:
                print(f"Error mapping shift type: {e}")
                return  
            
            if shift_type_code:
                date_range = self.generate_date_range(start_date, end_date, shift_type_account_weekend)
                duration = self.format_duration_to_hhcc(float(row[6]), len(date_range))

                for date in date_range:
                    giotto_line = f"{company_id};;01;{worker_id};{date};{shift_type_code};{duration};{duration_type}"
                    giotto_lines.append(giotto_line)

        # Not to save the file in the server, just at CLient's downloads folder
        output = io.StringIO()  # Create an in-memory file
        output.write("\n".join(giotto_lines))  
        csv_content = output.getvalue()
        output.close()

        return csv_content  # Return the CSV data as a string

    def convert_data(self, data):        
        csv_content = self.convert_format_to_giotto(data)
        return csv_content

