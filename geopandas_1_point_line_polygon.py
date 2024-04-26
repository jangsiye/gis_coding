from shapely.geometry import Polygon, LineString, Point
import matplotlib.pyplot as plt

# ============= Point 데이터 생성 =============
# 임의의 Point 데이터 생성
points = [Point(0, 0), Point(1, 2), Point(2, 1), Point(3, 3), Point(4, 2), Point(5, 0)]

# 그리기
x_coords = [point.x for point in points]
y_coords = [point.y for point in points]
plt.scatter(x_coords, y_coords, c='blue', marker='o')  # 점을 파란색 원으로 표시
plt.title('Points')

plt.show()

# ============= LineString 데이터 생성 =============
# 임의의 LineString 데이터 생성
lines = [
    LineString([(0, 0), (1, 2), (2, 1), (3, 3), (4, 2), (5, 0)]),  # 첫 번째 라인
    LineString([(0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (5, 3)])   # 두 번째 라인, y축 값이 더 높음
]

# 서브플롯 준비
fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1행 2열 서브플롯 생성

# 첫 번째 서브플롯: LineString 그리기
for line in lines:
    x, y = line.xy
    axs[0].plot(x, y, marker='o')  # 점과 선으로 그림
axs[0].set_aspect('equal')
axs[0].set_title('LineString')

# 두 번째 서브플롯: Line to Point 그리기
points = [Point(coord) for line in lines for coord in line.coords]
x_coords = [point.x for point in points]
y_coords = [point.y for point in points]
axs[1].scatter(x_coords, y_coords, c='blue', marker='o')  # 점을 파란색 원으로 표시
axs[1].set_aspect('equal')
axs[1].set_title('LineString to Points')

plt.show()

# ============= polygon 데이터 생성 =============
# 임의의 Polygon 데이터 생성
polygons = [
    Polygon([(0, 0), (2, 3), (4, 0), (3, -1), (1, -1)]),  # 복잡한 다각형
    Polygon([(5, 0), (6, 3), (8, 3), (9, 0)]),  # 사다리꼴
    Polygon([(10, 0), (10, 3), (12, 3), (13, 2), (12, 0)])  # 기울어진 사각형
]

# 각 Polygon마다 다른 색상으로 점 표시
colors = ['blue', 'green', 'red']

# 서브플롯 준비
fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1행 2열 서브플롯 생성

# polygon을 그래프로 그리기
for polygon, color in zip(polygons, colors):
        x, y = polygon.exterior.xy      # 폴리곤은 exterior 속성을 사용
        axs[0].plot(x, y, c=color)
axs[0].set_aspect('equal')
axs[0].set_title('Polygon')

# polygon을 point로 분해해서 그래프로 그리기
for idx, polygon in enumerate(polygons):
    # 각 Polygon의 점들을 Point로 변환
    points = [Point(coord) for coord in polygon.exterior.coords]
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    axs[1].scatter(x_coords, y_coords, color=colors[idx], label=f'Polygon {idx+1}', marker='o')
axs[1].set_aspect('equal')
axs[1].set_title('Polygon to Points')

plt.show()
