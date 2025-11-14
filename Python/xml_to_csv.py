import os
import csv
import sys

# QGIS環境のパス設定
sys.path.append(r"C:\Program Files\QGIS 3.36.2\apps\qgis\python")
sys.path.append(r"C:\Program Files\QGIS 3.36.2\apps\Python39\Lib\site-packages")

from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsProject,
    QgsCoordinateTransform,
    QgsGeometry
)
from qgis.analysis import QgsNativeAlgorithms

# QGISアプリケーションの初期化
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.36.2\apps\qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# パスの設定（必要に応じて変更）
input_dir = r"C:\Users\kyohe\石川県基盤地図情報\建物ポリゴン\building_polygon"
output_csv = r"C:\Users\kyohe\Ishikawa_KibanChizu_Analysis\building_area_csv\building_area_summary.csv"

print(f"入力ディレクトリ: {input_dir}")
print(f"出力CSVファイル: {output_csv}")

# 出力ディレクトリが存在しない場合は作成
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# 投影先CRS（JGD2011の平面直角座標系7系など）
target_crs = QgsCoordinateReferenceSystem("EPSG:6677")

# 入力ファイルの一覧を取得
xml_files = [f for f in os.listdir(input_dir) if f.endswith(".xml")]
print(f"処理対象のXMLファイル数: {len(xml_files)}")

with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ファイル名', 'ポリゴンID', '面積(m2)'])

    for filename in xml_files:
        print(f"\n処理開始: {filename}")
        path = os.path.join(input_dir, filename)
        layer = QgsVectorLayer(path, filename, "ogr")

        if not layer.isValid():
            print(f"{filename} 読み込み失敗")
            continue

        print(f"レイヤー読み込み成功: {layer.featureCount()} 個のフィーチャー")
        print(f"元のCRS: {layer.crs().description()}")

        # 投影変換
        try:
            # 座標変換オブジェクトの作成
            transform = QgsCoordinateTransform(
                layer.crs(),
                target_crs,
                QgsProject.instance()
            )
            
            feature_count = 0
            for feature in layer.getFeatures():
                geom = feature.geometry()
                if geom:
                    # ジオメトリを新しいCRSに変換
                    transformed_geom = QgsGeometry(geom)
                    transformed_geom.transform(transform)
                    
                    # 面積の計算（変換後のジオメトリを使用）
                    area = transformed_geom.area()
                    fid = feature['fid'] if 'fid' in feature.fields().names() else feature.id()
                    writer.writerow([filename, fid, round(area, 2)])
                    feature_count += 1
            
            print(f"処理完了: {feature_count} 個のフィーチャーを処理")

        except Exception as e:
            print(f"{filename} の投影変換エラー: {e}")
            continue

print("\n全ての処理が完了しました。")
# QGISアプリケーション終了
qgs.exitQgis()
