from bs4 import BeautifulSoup
import requests
import pandas as pd

# I tried to integrate a separate geo plot for India but ran out of time :/
coords = {"Andaman and Nicobar Islands": [11.7400867, 92.6586401],
          "Andhra Pradesh": [15.9129, 79.7400],
          "Arunachal Pradesh": [28.0000, 95.0000],
          "Assam": [26.2006043, 92.9375739],
          "Bihar": [25.18333333, 85.5333333],
          "Chandigarh": [30.73722222, 76.78722222],
          "Chhattisgarh": [21.5000, 82.0000],
          "Dadar Nagar Haveli": [30.700000, 76.90000000],
          "Delhi": [28.38, 77.12],
          "Goa": [28.63333333, 72.20000000],
          "Gujarat": [23.00, 72.00],
          "Haryana": [30.3, 74.6],
          "Himachal Pradesh": [32.48333333, 75.16666667],
          "Jammu and Kashmir": [32.73333333, 74.90000000],
          "Jharkhand": [23.73333333, 85.50000000],
          "Karnataka": [15.000, 75.00],
          "Kerala": [10, 76.41666667],
          "Ladakh": [34.152588, 77.577049],
          "Madhya Pradesh": [23.50000000, 80.000],
          "Maharashtra": [20.00, 76.00],
          "Manipur": [24.73333333, 93.96666667],
          "Meghalaya": [25.50, 91.00],
          "Mizoram": [23.50000000, 20.86666667],
          "Odisha": [26.00, 94.33333333],
          "Puducherry": [11.93333333, 79.88333333],
          "Punjab": [30.06666667, 75.08333333],
          "Rajasthan": [27.00, 74.00],
          "Tamil Nadu": [11.00, 78.00],
          "Telengana": [18.1124, 79.0193],
          "Tripura": [23.75000000, 91.50000000],
          "Uttarakhand": [30.25000000, 79.25000000],
          "Uttar Pradesh": [27.66666667, 80.000],
          "West Bengal": [23.00, 87.00]}


def get_indian_map_details():
    URL = 'https://www.mohfw.gov.in/'
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    header = extract_contents(soup.tr.find_all('th'))
    stats = []
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            if len(stat) == 5:
                if stat[1] in coords:
                    stat = [stat[0], stat[1], stat[2], stat[4], coords[stat[1]][0], coords[stat[1]][1]]
                    stats.append(stat)
    stats = stats[:-2]
    columns = ["Sno", "State", "Confirmed", "Deaths", "Lat", "Long"]
    df = pd.DataFrame(stats, columns=columns)
    return df

# get_indian_map_details()
