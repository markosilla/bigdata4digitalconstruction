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

# filename,ehitisePindala,ehitiseMaht,ehitisalunePind,suletud_netopind,energiaKlass,mahtBruto,maxKorrusteArv,yldkasut_pind,esmane_kasutus
# 103014811.ehr.json,3229.4,11903.0,722.0,3229.4,E,11903.0,5,410.7,1975
# 103015648.ehr.json,3757.7,12450.0,804.7,3757.7,D,12450.0,5,713.8,1976
# 103015786.ehr.json,3220.4,11671.0,711.0,3220.4,D,11671.0,5,432.7,1999
# 104018086.ehr.json,9860.5,33240.0,1258.0,9860.5,D,33240.0,9,1888.3,1995
# 104018213.ehr.json,4989.8,17111.0,664.0,4989.8,D,17111.0,9,645.3,1989
# 104018376.ehr.json,7950.8,16000.0,500.0,7950.8,D,16000.0,9,,1995
# 104019313.ehr.json,4988.3,17111.0,657.0,4988.3,D,17111.0,9,1021.1,1990
# 104023804.ehr.json,9890.2,34109.0,1246.0,9890.2,E,34109.0,9,1005.6,1989
# 104036004.ehr.json,5003.3,17111.0,657.0,5003.3,D,17111.0,9,570.8,1989
# 121363179.ehr.json,650.0,2584.0,356.0,650.0,A,2584.0,3,83.2,2023
# 121363182.ehr.json,632.4,2528.0,336.0,632.4,A,2528.0,3,79.3,2023
# 121363185.ehr.json,616.3,2465.0,315.0,616.3,A,2465.0,3,73.0,2023

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
