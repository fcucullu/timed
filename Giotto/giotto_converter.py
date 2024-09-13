import pandas as pd
import os
import json
from datetime import datetime, timedelta

def load_shift_type_mapping(mapping_file):
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            shift_type_mapping = json.load(f)
        return shift_type_mapping
    except Exception as e:
        print(f"Error loading JSON mapping file: {e}")
        return {}

def format_duration_to_hhcc(duration, date_range_length):
    duration_per_day = duration / date_range_length
    hours = int(duration_per_day)
    minutes = int((duration_per_day - hours) * 100)
    return f"{hours:02}{minutes:02}"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')

def generate_date_range(start_date, end_date, shift_type_account_weekend):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    date_range = [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]

    if not shift_type_account_weekend:
        # Filter out weekends if weekends should not be counted
        date_range = [date for date in date_range 
                      if (start + timedelta(days=int(date) - int(date_range[0]))).weekday() < 5]
    return date_range

def convert_format_to_giotto(data, shift_type_mapping):
    giotto_lines = []
    
    for row in data:
        company_id = row[1]  
        worker_id = row[2]  
        start_date = row[3]  
        end_date = row[4]  
        shift_type = row[5]  
        duration_type = '2'  

        try:
            shift_type = shift_type_mapping.get(shift_type)
            shift_type_code = shift_type[0]
            shift_type_account_weekend = shift_type[1]
        except Exception as e:
            print(f"Error loading shift type mapping file: {e}")
            #return
        
        if shift_type_code:
            date_range = generate_date_range(start_date, end_date, shift_type_account_weekend)
            duration = format_duration_to_hhcc(float(row[6]), len(date_range))
            for date in date_range:
                giotto_line = f"{company_id};;01;{worker_id};{date};{shift_type_code};{duration};{duration_type}"
                giotto_lines.append(giotto_line)

    with open("giotto_output.csv", "w") as f:
        f.write("\n".join(giotto_lines))

    print("Giotto output generated successfully.")
    return


current_dir = os.getcwd()
file_path = current_dir + r'\timed\Giotto\origin\Vp store srl.csv'  
mapping_file = current_dir + r'\timed\\Giotto\utils\shift_type_mapping.json' 

data = pd.read_csv(file_path).values.tolist()

shift_type_mapping = load_shift_type_mapping(mapping_file)

convert_format_to_giotto(data, shift_type_mapping)
