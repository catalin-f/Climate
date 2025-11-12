#!/usr/bin/python3

import requests 
import json


# API endpoint
url = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    data = response.json()

    # Display the structure and a sample
    print(json.dumps(data, indent=4, ensure_ascii=False))


    for i in data["features"]:
        if i["properties"]["nume"]=="BUCURESTI FILARET":
            print(i["properties"]["tempe"])
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")

