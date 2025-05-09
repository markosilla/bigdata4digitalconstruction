import os
import json
import pandas as pd

# Define the folder containing JSON files
folder = "ehr_files"

def extract_nested_values(data):
    """ Extract values from nested JSON fields with deep search for esmane_kasutus and suletud_netopind. """
    ehitis = data[0].get("ehitis", {}) if isinstance(data, list) and len(data) > 0 else {}

    extracted_values = {
        "filename": None,  
        "ehitisePindala": ehitis.get("ehitisePohiandmed", {}).get("suletud_netopind"),
        "ehitiseMaht": ehitis.get("ehitisePohiandmed", {}).get("mahtBruto"),
        "ehitisalunePind": ehitis.get("ehitisePohiandmed", {}).get("ehitisalunePind"),
        "suletud_netopind": ehitis.get("ehitisePohiandmed", {}).get("suletud_netopind"),
        "energiaKlass": None,
        "mahtBruto": ehitis.get("ehitisePohiandmed", {}).get("mahtBruto"),
        "maxKorrusteArv": ehitis.get("ehitisePohiandmed", {}).get("maxKorrusteArv"),
        "yldkasut_pind": ehitis.get("ehitisePohiandmed", {}).get("yldkasut_pind"),
        "esmane_kasutus": None
    }

    # Extract energiaKlass from "ehitiseEnergiamargised"
    energiamargised = ehitis.get("ehitiseEnergiamargised", {}).get("energiamargis", [])
    if isinstance(energiamargised, list) and len(energiamargised) > 0:
        energia_value = energiamargised[0].get("energiaKlass")
        if isinstance(energia_value, str) and energia_value:
            extracted_values["energiaKlass"] = energia_value[0]  # Extract only the first letter

    # Deep search function to find specific fields anywhere in JSON
    def deep_search(obj, key_to_find):
        """ Recursively search for a specific key in all dictionaries and lists. """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == key_to_find and value not in [None, ""]:
                    return value  # Return the first valid value found
                if isinstance(value, (dict, list)):
                    result = deep_search(value, key_to_find)
                    if result:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = deep_search(item, key_to_find)
                if result:
                    return result
        return None

    # Perform deep search for the required field
    extracted_values["esmane_kasutus"] = deep_search(data, "esmaneKasutus")

    return extracted_values

def extract_values_from_all_files(folder):
    """ Scans all JSON files in the given folder and extracts relevant data. """
    extracted_data = []

    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        return None

    for filename in os.listdir(folder):
        if filename.endswith(".ehr.json"):
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                extracted_entry = extract_nested_values(data)
                extracted_entry["filename"] = filename  # Add filename to the extracted data
                extracted_data.append(extracted_entry)

    # Convert to a DataFrame for structured output
    df = pd.DataFrame(extracted_data)
    return df

# Run extraction
df_result = extract_values_from_all_files(folder)

# Display extracted data in **comma-separated format** for easy copy-paste into Excel
if df_result is not None:
    print(df_result.to_csv(index=False))  # Comma-separated output
