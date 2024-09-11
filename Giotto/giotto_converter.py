import pandas as pd
import os
import json
from datetime import datetime, timedelta

def load_absence_mapping(mapping_file):
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            absence_mapping = json.load(f)
        return absence_mapping
    except Exception as e:
        print(f"Error loading JSON mapping file: {e}")
        return {}

def format_duration_to_hhmm(duration):
    hours = int(duration)
    minutes = int((duration - hours) * 60)
    return f"{hours:02}{minutes:02}"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')

def generate_date_range(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    return [(start + timedelta(days=i)).strftime('%Y%m%d') for i in range((end - start).days + 1)]

def convert_format_to_giotto(data, shiftType_mapping_file):
    giotto_lines = []
    
    for row in data:
        employerId = row[1]  # 'Identificatore aziendale (paghe)'
        workerId = row[2]  # 'Identificatore dipendente (paghe)'
        startDate = row[3]  # 'Data di inizio dell'assenza'
        endDate = row[4]  # 'Data di fine dell'assenza'
        shiftType = row[5]  # 'Tipologia di assenza'
        duration = format_duration_to_hhmm(float(row[6]))  # 'Durata dell'assenza'
        durationType = '2'  # 'Tipologia di durata' (constant as '2')

        # Map the absence type to the destination format
        mapped_absence_type = shiftType_mapping_file.get(shiftType, 'UNK')  # Default to 'UNK' if not found
        
        # Generate date range from start to end date
        date_range = generate_date_range(startDate, endDate)
        
        # Create a Giotto formatted line for each date in the range
        for date in date_range:
            giotto_line = f"{employerId};;01;{workerId};{date};{mapped_absence_type};{duration};{durationType}"
            giotto_lines.append(giotto_line)

    # Write the Giotto formatted lines to a file
    with open("giotto_output.csv", "w") as f:
        f.write("\n".join(giotto_lines))

    print("Giotto output generated successfully.")


# Example usage:
current_dir = os.getcwd()
file_path = current_dir + r'\Giotto\origin\Vp store srl.csv'  
mapping_file = current_dir + r'\Giotto\utils\shiftType_mapping.json' 

# Load the CSV data
data = pd.read_csv(file_path).values.tolist()

# Load the absence mapping from the JSON file
absence_mapping = load_absence_mapping(mapping_file)

# Convert the data and generate Giotto output
convert_format_to_giotto(data, absence_mapping)
