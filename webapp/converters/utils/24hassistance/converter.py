# %%
import pandas as pd

# Define the field structure
fields = [
    {"name": "Vuoto", "start": 1, "length": 3},
    {"name": "Codice Azienda", "start": 4, "length": 6},
    {"name": "Codice Sede", "start": 10, "length": 4},
    {"name": "Dipendente", "start": 14, "length": 6},
    {"name": "Causale", "start": 20, "length": 5},
    {"name": "Data", "start": 25, "length": 10},
    {"name": "Unita di misura", "start": 35, "length": 1},
    {"name": "Tariffa", "start": 36, "length": 10},
    {"name": "Quantita", "start": 46, "length": 10},
    {"name": "Risultato", "start": 56, "length": 10},
    {"name": "Ore Teoriche", "start": 66, "length": 4},
    {"name": "Tipo movimento", "start": 70, "length": 1},
    {"name": "Inizio Evento", "start": 71, "length": 1},
]

# Specify the file name
file_name = "gispaghes_Report Brooktec (1)_202311140546 (2) (1) (1).txt"

# Read the file and load its contents
with open(file_name, "r") as file:
    data = file.readlines()

# Function to parse the string dynamically based on the fields structure
def parse_string(row, fields):
    parsed_row = []
    for field in fields:
        start = field["start"] - 1  # Convert 1-based to 0-based indexing
        length = field["length"]
        raw_value = row[start:start + length]
        parsed_row.append(raw_value)  # Keep raw value as string, preserving length
    return parsed_row

# Parse each row using the field definitions
parsed_data = [parse_string(row, fields) for row in data]

# Create a DataFrame with the field names as column headers
columns = [field["name"] for field in fields]
df = pd.DataFrame(parsed_data, columns=columns)

# Display the DataFrame in Variable Explorer
print(df)
# %%
