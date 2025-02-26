import requests
import json
import os

def fetch_building_data(building_id):
    # URL of the API endpoint
    url = 'https://devkluster.ehr.ee/api/building/v2/buildingsData'

    # Headers to specify that we accept JSON and will send JSON
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Data payload with the building ID
    payload = {
        'ehrCodes': [building_id]  # This assumes the API expects a list, even for a single ID
    }

    # Making the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors or unsuccessful responses
        print(f"Error fetching data: {response.status_code}")
        return None

def save_data_to_file(building_id, data, folder="ehr_files"):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)
    
    # Construct the full file path
    filename = os.path.join(folder, f"{building_id}.ehr.json")

    # Save the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to {filename}")

# 222	marko.silla@taltech.ee	2025K	121363179	Pärnu	Rääma tn 9
# 222	marko.silla@taltech.ee	2025K	121363182	Pärnu	Rääma tn 9a
# 222	marko.silla@taltech.ee	2025K	121363185	Pärnu	Rääma tn 11
# 223	marko.silla@taltech.ee	2025K	103014811	Pärnu	Mai 39
# 223	marko.silla@taltech.ee	2025K	103015648	Pärnu	Mai45
# 223	marko.silla@taltech.ee	2025K	103015786	Pärnu	Mai 43
# 224	marko.silla@taltech.ee	2025K	104018086	Tartu	Mõisavahe 35
# 224	marko.silla@taltech.ee	2025K	104018376	Tartu	Mõisavahe 38
# 224	marko.silla@taltech.ee	2025K	104023804	Tartu	Mõisavahe 42
# 225	marko.silla@taltech.ee	2025K	104018213	Tartu	Mõisavahe 43
# 225	marko.silla@taltech.ee	2025K	104019313	Tartu	Mõisavahe 47
# 225	marko.silla@taltech.ee	2025K	104036004	Tartu	Mõisavahe 39

if __name__ == "__main__":
    building_ids = ["121363179",
"121363182",
"121363185",
"103014811",
"103015648",
"103015786",
"104018086",
"104018376",
"104023804",
"104018213",
"104019313",
"104036004"]
    for building_id in building_ids:
        print(f"Fetching data for Building ID: {building_id}")
        data = fetch_building_data(building_id)
        if data is not None:
            save_data_to_file(building_id, data)
