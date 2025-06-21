from qgis.core import QgsVectorLayer, QgsProject

EVENTS_LAYER_NAME = "events"

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

project = QgsProject.instance()
layer = project.mapLayersByName("adm0")[0]
layer.setSubsetString("iso3 = 'NPL'")

extent = layer.extent()

min_lon = extent.xMinimum()
min_lat = extent.yMinimum()
max_lon = extent.xMaximum()
max_lat = extent.yMaximum()

start_date = "2010-01-01"
end_date = "2025-07-06"

min_magnitude = 5

params = dict(
    format="geojson",
    starttime=start_date,
    minmagnitude=min_magnitude,
    endtime=end_date,
    minlongitude=min_lon,
    maxlongitude=max_lon,
    minlatitude=min_lat,
    maxlatitude=max_lat,
)

params_str = "&".join([f"{k}={v}" for k,v in params.items()])

url = f"{API_URL}?{params_str}"

[project.removeMapLayer(e) for e in project.mapLayersByName(EVENTS_LAYER_NAME)]

events_layer = QgsVectorLayer(url, EVENTS_LAYER_NAME, "ogr")

is_valid = layer.isValid()

map_layer = project.addMapLayer(events_layer)
canvas = iface.mapCanvas()
canvas.setExtent(extent)

