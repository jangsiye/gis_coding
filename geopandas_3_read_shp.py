import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np
import os, sys

# ============= 1. point 데이터 읽기 =============
# Shapefile 읽고 geometry 열에서 Point 데이터 추출
gdf = gpd.read_file("./data/A1_NODE.shp")
print(type(gdf.geometry[0]))
print(gdf.geom_type)

# numpy array로 변환
# points = np.array([(point.x, point.y) for point in gdf.geometry])
# print(points)

# ============= 2. line 데이터 읽기 =============
gdf = gpd.read_file("./data/A2_LINK.shp")
print(type(gdf.geometry[0]))
print(gdf.geom_type)

# numpy array로 변환
# coordinates_array = np.vstack([np.array(line.coords) for line in gdf.geometry])
# print(coordinates_array)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1행 2열 서브플롯 생성
# line 그래프로 그리기
for linestring in gdf.geometry:
    x, y = linestring.xy
    axs[0].plot(x, y, marker='o')  # 점과 선으로 그림
axs[0].set_aspect('equal')  # 축 비율 설정
axs[0].set_title('Line Plot')

# line to point 그래프로 그리기
points = [Point(coord) for linestring in gdf.geometry for coord in linestring.coords]
x_coords = [point.x for point in points]
y_coords = [point.y for point in points]
axs[1].scatter(x_coords, y_coords, c='blue', marker='o')  # 점을 파란색 원으로 표시
axs[1].set_aspect('equal')  # 축 비율 설정
axs[1].set_title('Line to Point Plot')

plt.show()

# ============= 3. polygon 데이터 읽기 =============
gdf = gpd.read_file("./data/C4_SPEEDBUMP.shp")
print(type(gdf.geometry[0]))
print(gdf.geom_type)

# numpy array로 변환
# exterior_coords = np.vstack([np.array(polygon.exterior.coords) for polygon in gdf.geometry])
# print(exterior_coords)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1행 2열 서브플롯 생성

# polygon을 그래프로 그리기
for polygon in gdf.geometry:
        x, y = polygon.exterior.xy
        axs[0].plot(x, y, c='blue')
axs[0].set_aspect('equal')  # 축 비율 설정
axs[0].set_title('Polygon Plot')

# polygon to point 그래프로 그리기
points = [Point(coord) for polygon in gdf.geometry for coord in polygon.exterior.coords]
x_coords = [point.x for point in points]
y_coords = [point.y for point in points]
axs[1].scatter(x_coords, y_coords, c='blue', marker='o')  # 점을 파란색 원으로 표시
axs[1].set_aspect('equal')  # 축 비율 설정
axs[1].set_title('Polygon to Point Plot')

plt.show()
