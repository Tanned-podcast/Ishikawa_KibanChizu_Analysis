import sys
sys.path.append(r"C:\Program Files\QGIS 3.36.2\apps\qgis\python")
sys.path.append(r"C:\Program Files\QGIS 3.36.2\apps\Python39\Lib\site-packages")

from qgis.core import QgsApplication, QgsVectorLayer
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.36.2\apps\qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

path = r"C:\Users\kyohe\石川県基盤地図情報\建物ポリゴン\building_polygon"
filename = "FG-GML-543605-BldA-20250101-0001.xml"

layer = QgsVectorLayer(path, filename, "ogr")

print("QGIS is working")

qgs.exitQgis()