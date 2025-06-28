import requests
from csv import DictReader
from datetime import datetime, date

EVENTS_LAYER_NAME = "events"
BOUNDARIES_LAYER_NAME = "boundaries"

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
BOUNDARIES_URL = "https://raw.githubusercontent.com/WFP-VAM/prism-app/refs/heads/master/frontend/public/data/global/adm0_simplified.json"

FIELDS = [
    QgsField("id", QVariant.String),
    QgsField("time", QVariant.String),
    QgsField("depth", QVariant.Double),
    QgsField("mag", QVariant.Double),
]


def get_api_features(extent, start_date, end_date, min_magnitude):
    min_lon = extent.xMinimum()
    min_lat = extent.yMinimum()
    max_lon = extent.xMaximum()
    max_lat = extent.yMaximum()

    params = dict(
        format="csv",
        starttime=start_date,
        minmagnitude=min_magnitude,
        endtime=end_date,
        minlongitude=min_lon,
        maxlongitude=max_lon,
        minlatitude=min_lat,
        maxlatitude=max_lat,
    )

    resp = requests.get(API_URL, params=params)
    resp.raise_for_status()

    decoded_content = resp.content.decode("utf-8").splitlines()

    rows = [r for r in DictReader(decoded_content)]

    return rows


def create_qgis_feature(fields, row):
    feature = QgsFeature()

    x = float(row["longitude"])
    y = float(row["latitude"])

    point = QgsPointXY(x, y)

    geom = QgsGeometry.fromPointXY(point)

    values = [row[f.name()] for f in fields]

    feature.setAttributes(values)
    feature.setGeometry(geom)

    return feature


boundaries_layer = QgsVectorLayer(BOUNDARIES_URL, BOUNDARIES_LAYER_NAME, "ogr")
boundaries_layer.setSubsetString("iso3 = 'DOM'")

extent = boundaries_layer.extent()

end_date = date.today().isoformat()

api_features = get_api_features(extent, "2010-01-01", end_date, 5)

events_layer = QgsVectorLayer("Point", EVENTS_LAYER_NAME, "memory")
provider = events_layer.dataProvider()

provider.addAttributes(fields)
events_layer.updateFields()

features = [create_qgis_feature(fields, r) for r in api_features]
provider.addFeatures(features)
events_layer.updateExtents()


project = QgsProject.instance()
project.addMapLayer(boundaries_layer)
project.addMapLayer(events_layer)
canvas = iface.mapCanvas()
canvas.setExtent(extent)
