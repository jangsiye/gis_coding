
# 공간 분석 - 관계 연산 예시

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import os, sys

# 샘플 데이터셋 로드
countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

print(countries.head())
print(cities.head())
print(countries.geometry.head())
print(cities.geometry.head())

# 도시 뭐 있는지 한 번 쭉 보기
print(cities['name'])

# 국가 : 캐나다, 미국 추출
two_country = countries.loc[countries['name'].isin(['Canada', 'United States of America'])]
base = two_country.plot(figsize=(15, 15), color="w", edgecolor="m")

# 도시 : 벤쿠버, 토론토, 뉴욕 추출
vancouver = cities.loc[cities.name == "Vancouver", "geometry"].squeeze()
toronto = cities.loc[cities.name == "Toronto", "geometry"].squeeze()
newyork = cities.loc[cities.name == "New York", "geometry"].squeeze()
line = LineString([vancouver, toronto, newyork])

ax = gpd.GeoSeries([vancouver, toronto, newyork, line]).plot(ax=base)
ax.set_title("North America Citys")
plt.show()

# ========================================================================================
# 관계 연산자
canada = countries.loc[countries['name'] == 'Canada', 'geometry'].squeeze()
us = countries.loc[countries['name'] == 'United States of America', 'geometry'].squeeze()

# g1.within(g2) : 한 공간(g1)이 다른 공간(g2)에 포함되면 True
# 미국은 뉴욕을 포함하고 있다
print(newyork.within(us))

# g2.contains(g1) : 한 공간(g2)이 다른 공간(g1)에 포함되면 True
# 뉴욕은 미국을 포함하고 있다
print(us.contains(newyork))

# g1.intersects(g2) : 두 공간의 교집합 영역이 존재하면 Ture (점 또는 선도 포함)
# 미국과 캐나다는 국경을 맞대고 있다 (교집합이 존재한다)
print(canada.intersects(us))

# l1.crosses(g1) : 라인이 공간을 가로지르면 True
# 벤쿠버와 뉴욕를 잇는 선은 미국을 가로지른다
print(line.crosses(us))

# bool 연산자 이기 때문에 데이터 검색도 가능하다
# 벤쿠버와 상파울로를 잇는 선에 있는 나라들은?
vancouver = cities.loc[cities.name == "Vancouver", "geometry"].squeeze()
saopaulo = cities.loc[cities.name == "São Paulo", "geometry"].squeeze()
line = LineString([vancouver, saopaulo])
print(countries[countries.intersects(line)])

# g1.distance(g2) : 두 공간의 거리
# 뉴욕과 상파울로의 거리
print(newyork.distance(saopaulo))
# 미국과 캐나다의 거리  --> 가장 가까운 거리를 구해준다
print(canada.distance(us))

# 캐나다의 면적 구하기
print(canada.area)

# 캐나다의 국경 그리기
border = canada.boundary
print(type(border))

# MultiLineString 그리기
for line in border.geoms:
    x, y = line.xy
    plt.title("Canada Border")
    plt.plot(x, y, 'o-')  # 'o-'는 각 선에 점을 포함하여 선을 그림
plt.show()
