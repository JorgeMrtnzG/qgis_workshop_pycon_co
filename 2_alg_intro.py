from qgis.processing import alg

@alg(
    name="Example Processing function",
    label="Example processing function label",
    group="general",
    group_label="General",
)
@alg.input(type=alg.EXTENT, name="extent", label="extent")
@alg.input(
    type=alg.DATETIME,
    name="date",
    label="Date"
)
@alg.output(type=alg.STRING, name="out_date", label="out_date")
@alg.output(type=alg.NUMBER, name="area", label="area")
def create_usgs_layer(instance, parameters, context, feedback, inputs):
    """This is a simple demo"""
    extent = instance.parameterAsExtent(parameters, "extent", context)
    date = instance.parameterAsDateTime(parameters, "date", context)

    return {"out_date": date.toString(), "area": extent.area()}
