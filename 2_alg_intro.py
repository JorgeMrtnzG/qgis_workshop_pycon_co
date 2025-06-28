import requests
from csv import DictReader
from qgis.core import *
from qgis.processing import alg
from datetime import datetime, timedelta
from PyQt5.QtCore import QVariant


END_DATE = datetime.now()
START_DATE = (END_DATE - timedelta(days=365 * 10)).replace(month=1, day=1)

EVENTS_LAYER_NAME = "events"
API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

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
        starttime=start_date.date(),
        minmagnitude=min_magnitude,
        endtime=end_date.date(),
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


@alg(
    name="USGS download",
    label="Download USGS events",
    group="general",
    group_label="General",
)
@alg.input(type=alg.EXTENT, name="extent", label="extent")
@alg.input(type=alg.INT, name="min_mag", label="Min magnitude", default=5)
@alg.input(
    type=alg.DATETIME,
    name="start_date",
    label="End date",
    default=START_DATE.isoformat(),
)
@alg.input(
    type=alg.DATETIME, name="end_date", label="Start date", default=END_DATE.isoformat()
)
@alg.input(type=alg.SINK, name=EVENTS_LAYER_NAME, label=EVENTS_LAYER_NAME)
def create_usgs_layer(instance, parameters, context, feedback, inputs):
    """This is a simple demo"""

    extent = instance.parameterAsExtent(parameters, "extent", context)
    min_mag = instance.parameterAsInt(parameters, "min_mag", context)

    start_date = instance.parameterAsDateTime(parameters, "start_date", context)
    end_date = instance.parameterAsDateTime(parameters, "end_date", context)

    start_date = start_date.toPyDateTime()
    end_date = end_date.toPyDateTime()

    api_features = get_api_features(extent, start_date, end_date, min_mag)
    features = [create_qgis_feature(FIELDS, r) for r in api_features]

    fields = QgsFields()
    [fields.append(f) for f in FIELDS]

    (sink, dest_id) = instance.parameterAsSink(
        parameters,
        EVENTS_LAYER_NAME,
        context,
        fields,
        QgsWkbTypes.Point,
        QgsCoordinateReferenceSystem("EPSG:4326"),
    )

    [sink.addFeature(f, QgsFeatureSink.FastInsert) for f in features]

    return {EVENTS_LAYER_NAME: dest_id}
