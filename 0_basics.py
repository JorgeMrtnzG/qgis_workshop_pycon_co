url = "https://raw.githubusercontent.com/WFP-VAM/prism-app/refs/heads/master/frontend/public/data/global/adm0_simplified.json"

layer = QgsVectorLayer(url, "boundaries", "ogr")
layer.setSubsetString("iso3 = 'PSE'")

project = QgsProject.instance()

project.addMapLayer(layer)
