import requests
from qgis.processing import alg
from datetime import datetime, timedelta

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

today = datetime.now()
delta = today - timedelta(days=365 * 20)


@alg(
    name="USGS download",
    label="Download USGS events",
    group="general",
    group_label="General",
)
@alg.input(type=alg.EXTENT, name="extent", label="extent")
@alg.input(type=alg.INT, name="min_mag", label="Min magnitude", default=5)
@alg.input(type=alg.DATETIME, name="start_date", label="Start date", default=delta.isoformat())
@alg.input(type=alg.DATETIME, name="end_date", label="End date", default=today.isoformat())
@alg.input(type=alg.SINK, name="output", label="Output layer")
def download_usgs(instance, parameters, context, feedback, inputs):
    """ This is a simple demo """

    extent = instance.parameterAsExtent(parameters, "extent", context)
    min_mag = instance.parameterAsInt(parameters, "min_mag", context)
    
    start_date = instance.parameterAsDateTime(parameters, "start_date", context)
    end_date = instance.parameterAsDateTime(parameters, "end_date", context)
    
    start_date = start_date.toPyDateTime().date().isoformat()
    end_date = end_date.toPyDateTime().date().isoformat()
    
    min_lon = extent.xMinimum()
    min_lat = extent.yMinimum()
    max_lon = extent.xMaximum()
    max_lat = extent.yMaximum()
    
    params = dict(
        format="geojson",
        starttime=start_date,
        minmagnitude=min_mag,
        endtime=end_date,
        minlongitude=min_lon,
        maxlongitude=max_lon,
        minlatitude=min_lat,
        maxlatitude=max_lat,
    )
    
    resp = requests.get(API_URL, params=params)
    resp.raise_for_status()
    
    resp_json = resp.json()
    
    print(resp_json)


    return {}
