import pandas as pd
import os
import json
from datetime import datetime, timedelta

def load_shiftType_mapping(mapping_file):
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            shiftType_mapping = json.load(f)
        return shiftType_mapping
    except Exception as e:
        print(f"Error loading JSON mapping file: {e}")
        return {}

def format_duration_to_hhcc(duration, dateRangeLength):
    durationPerDay = duration / dateRangeLength
    hours = int(durationPerDay)
    minutes = int((durationPerDay - hours) * 100)
    return f"{hours:02}{minutes:02}"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')

def generate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]

def convert_format_to_giotto(data, shiftType_mapping):
    giotto_lines = []
    
    for row in data:
        employerId = row[1]  
        workerId = row[2]  
        startDate = row[3]  
        endDate = row[4]  
        shiftType = row[5]  
        durationType = '2'  

        try:
            shiftType = shiftType_mapping.get(shiftType)
        except Exception as e:
            print(f"Error loading shiftType mapping file: {e}")
            return
        
        date_range = generate_date_range(startDate, endDate)
        
        duration = format_duration_to_hhcc(float(row[6]), len(date_range))
        
        for date in date_range:
            giotto_line = f"{employerId};;01;{workerId};{date};{shiftType};{duration};{durationType}"
            giotto_lines.append(giotto_line)

    with open("giotto_output.csv", "w") as f:
        f.write("\n".join(giotto_lines))

    print("Giotto output generated successfully.")


current_dir = os.getcwd()
file_path = current_dir + r'\timed\Giotto\origin\Vp store srl.csv'  
mapping_file = current_dir + r'\timed\\Giotto\utils\shiftType_mapping.json' 

data = pd.read_csv(file_path).values.tolist()

shiftType_mapping = load_shiftType_mapping(mapping_file)

convert_format_to_giotto(data, shiftType_mapping)
