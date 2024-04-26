
# 두 개의 3차원 폴리곤을 가지고 분석

# 1) 2차원 / 3차원으로 그리기
# 2) z값으로 이상치 판별
# 3) 겹치는 영역 추출

import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import MultiPolygon, Polygon
import pandas as pd
import sys, os 

# 3D Polygon을 포함하는 MultiPolygon 생성
# 일반적인 높이값과 특정 폴리곤에 이상치 높이값을 설정
mp1 = [
    Polygon([(0, 0, 1), (2, 0, 1), (1.5, 1.5, 2), (0, 2, 2)]),  # 부분적으로 mp2의 첫 폴리곤과 겹침
    Polygon([(1, 1, 3), (2, 1, 3), (2.5, 2, 1), (1.5, 2.5, 1)])  # mp2의 두 번째 폴리곤과 약간 겹침
]

mp2 = [
    Polygon([(0.5, 0.5, 1), (1.5, 0.5, 1), (1, 1, 1), (0.5, 1.5, 1)]),  # mp1의 첫 번째 폴리곤과 부분 겹침
    Polygon([(1.5, 1.5, 2), (2.5, 1.5, 2), (3, 2.5, 2), (2, 3, 2)]),  # mp1의 두 번째 폴리곤과 부분 겹침
    Polygon([(0, 3, 10), (1, 3, 10), (1, 4, 15), (0, 4, 15)])  # 이상치 높이값을 가진 새 폴리곤 추가

]

# GeoDataFrame 생성
mark_1 = gpd.GeoDataFrame({
    'id': [46, 47],
    'geometry': mp1
}, crs='EPSG:4326')

mark_2 = gpd.GeoDataFrame({
    'id': [80, 81, 82],
    'geometry': mp2
}, crs='EPSG:4326')

# 데이터 확인
print(type(mark_1))
print(mark_1.head())
print(type(mark_2))
print(mark_2.head())

# # ======================================================================================================== 

# # 폴리곤 정보만 빼오기
mark_1_polygon = mark_1['geometry'].squeeze().reset_index(drop=True)
mark_2_polygon = mark_2['geometry'].squeeze().reset_index(drop=True)

# 두 폴리곤을 그래프로 그리기
ax = mark_1_polygon.plot(color='red', alpha=0.5)
mark_2_polygon.plot(ax=ax, color='blue', alpha=0.5)
plt.show()

# 멀티 폴리곤을 3D 그래프로 그리기
def plot_polygon_3d(ax, multipolygon, color):
    for polygon in multipolygon:
        x_values=([coord[0] for coord in polygon.exterior.coords])
        y_values=([coord[1] for coord in polygon.exterior.coords])
        z_values=([coord[2] for coord in polygon.exterior.coords])
        ax.plot(x_values, y_values, z_values, color=color, alpha=0.5)

# 3D 그래프 설정
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # Axes3D 객체 생성
# 3D 멀티 폴리곤 그리기
plot_polygon_3d(ax, mark_1_polygon, 'red')
plot_polygon_3d(ax, mark_2_polygon, 'blue')
plt.show()

# # ======================================================================================================== 

# mark_2_polygon에서 z값만 뽑아서 이상치 판별 하기
z_values = []
x_values = []
# MultiPolygon 경우
for polygon in mark_2_polygon:
    z_values.extend([coord[2] for coord in polygon.exterior.coords])
    x_values.extend([coord[0] for coord in polygon.exterior.coords])
    
print(max(z_values))
print(min(z_values))

from sklearn.linear_model import RANSACRegressor
import numpy as np

ransac = RANSACRegressor()
x_values = pd.DataFrame(x_values)
z_values = pd.DataFrame(z_values)
ransac.fit(x_values, z_values)

# 이상치가 아닌 데이터
inlier_mask = ransac.inlier_mask_
outlier_mask = ~inlier_mask

# 원래 데이터와 이상치를 그래프로 표시
plt.scatter(x_values[inlier_mask], z_values[inlier_mask], color='yellowgreen', marker='.', label='Inliers')
plt.scatter(x_values[outlier_mask], z_values[outlier_mask], color='gold', marker='.', label='Outliers')

# RANSAC에 의해 추정된 모델로 선 그리기
line_x_values = np.arange(x_values.min().item(), x_values.max().item())[:, np.newaxis]
line_z_values_ransac = ransac.predict(line_x_values)
plt.plot(line_x_values, line_z_values_ransac, color='cornflowerblue', linewidth=2, label='RANSAC regressor')
plt.title('mark_2 Z-value : RANSAC regressor')
plt.show()

# # ======================================================================================================== 

# 두 멀티 폴리곤 루프를 돌면서 겹치는 부분만 추출
inter_list = []
for poly1 in mark_1_polygon:
    for poly2 in mark_2_polygon:
        if poly1.intersects(poly2):
            inter_list.append(poly1.intersection(poly2))

intersection = gpd.GeoDataFrame(geometry=inter_list)

print(type(intersection))
print(intersection)

ax = mark_1.plot(color='red', alpha=0.5)
mark_2.plot(ax=ax, color='blue', alpha=0.5)
intersection.plot(ax=ax, color='green', alpha=0.5)
plt.show()
