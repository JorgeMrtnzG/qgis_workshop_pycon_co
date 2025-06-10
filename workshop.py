import requests

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

minlon = -81.8415714459999890
minlat = -4.2271099999999251
maxlon = -66.8463122879999787
maxlat = 13.3944826810000563

start_date = "2010-01-01"
end_date = "2025-07-06"

min_magnitude = 5

params = dict(
    format="geojson",
    starttime=start_date,
    minmagnitude=min_magnitude,
    endtime=end_date,
    minlongitude=minlon,
    maxlongitude=maxlon,
    minlatitude=minlat,
    maxlatitude=maxlat,
)

resp = requests.get(API_URL, params=params)
resp.raise_for_status()

print(resp.content.decode())



