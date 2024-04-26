import geopandas as gpd
from shapely.geometry import Polygon, LineString,Point
import matplotlib.pyplot as plt

# =========== shp, dbf, shx 파일 생성 예제 ===========
# Polygon 데이터 생성 (None은 빈 데이터를 의미)
data = [
        Polygon([(10, 0), (10, 3), (12, 3), (13, 2), (12, 0)]),
        None,
        Polygon([(0, 0), (2, 3), (4, 0), (3, -1), (1, -1)])
]

geo_dict = {'id': [45, 46, 47],
        'name': ['data A', 'data B', 'data C'],
        'geometry': data}

# GeoDataFrame 생성
# crs : 좌표계 변환 (EPSG:4326 -> 미국 주 좌표계(WGS84))
gdf = gpd.GeoDataFrame(geo_dict, crs='EPSG:4326')

# Shapefile로 저장
# 하나의 shp는 반드시 같은 타입의 데이터만 가질 수 있음
gdf.to_file("my_shapefile.shp")

# =========== shp 파일 읽기 예제 ===========
print("my_shapefile.shp 파일 내용")
# Shapefile 로드
gdf = gpd.read_file("./my_shapefile.shp")
# GeoDataFrame의 첫 몇 행을 출력
print(gdf.head())
# GeoDataFrame의 구조 및 데이터 타입 확인
print(gdf.info())

# =========== shp 파일 그래프로 그리기 ===========
# 점 데이터를 그래프로 그리기
gdf.plot(marker='o', color='blue', markersize=5)

# 그래프 설정
plt.title("Shapefile Point Plot")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# 표시
plt.show()
