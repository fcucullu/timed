import pandas as pd
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def load_file(file_path):
    # Get the file extension to determine if it's a CSV or Excel
    _, file_extension = os.path.splitext(file_path)
    
    try:
        if file_extension.lower() == '.csv':
            # Handle CSV file
            data = pd.read_csv(file_path, encoding='utf-8')  # Try 'utf-8' by default
            print("Loaded CSV file successfully.")
        elif file_extension.lower() in ['.xls', '.xlsx']:
            # Handle Excel file
            data = pd.read_excel(file_path)
            print("Loaded Excel file successfully.")
        else:
            raise ValueError("Unsupported file type.")
        
        # Convert the dataframe to a list of rows
        data_list = data.values.tolist()
        return data_list

    except UnicodeDecodeError:
        # If 'utf-8' encoding fails, retry with a different encoding
        try:
            if file_extension.lower() == '.csv':
                data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Fallback to ISO-8859-1
                print("Loaded CSV file with ISO-8859-1 encoding.")
                data_list = data.values.tolist()
                return data_list
            else:
                raise
        except Exception as e:
            print(f"Error reading file: {e}")
            return None


def convert_into_xml(list_of_lists):
    # Create root element of XML
    root = ET.Element("Employees")

    for entry in data:
        employee = ET.SubElement(root, "Employee", id=str(entry[0]))
        ET.SubElement(employee, "Name").text = entry[1]
        ET.SubElement(employee, "Lastname").text = entry[2]
        ET.SubElement(employee, "Start").text = entry[3].strftime('%d/%m/%Y %H:%M')
        ET.SubElement(employee, "End").text = entry[4].strftime('%d/%m/%Y %H:%M')
        ET.SubElement(employee, "Rate").text = str(entry[5])

    # Transform the XML tree to string
    xml_str = ET.tostring(root, encoding='unicode')

    # Usar minidom para formatear el XML
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    # Guardar el XML en un archivo
    with open("employees.xml", "w") as f:
        f.write(pretty_xml_str)

    print("XML generated successfully")




# Example usage:
file_path = 'original.xlsx'  # Replace with your file path
data = load_file(file_path)
convert_into_xml(data)