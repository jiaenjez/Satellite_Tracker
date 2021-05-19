from src import location_input
import requests

"""
for testing location_input
"""

url = location_input.getURL()
print(url)
response = requests.get(url).json()
print("UCI:", response["resourceSets"][0]["resources"][0]["point"]["coordinates"])
