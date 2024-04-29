
# ply 파일을 읽어서 포인트 클라우드 데이터를 출력하고 시각화하는 예제

import numpy as np
import open3d as o3d

# Read .ply file
input_file = "D:/images/Toronto_3D/L004.ply"
pcd = o3d.io.read_point_cloud(input_file) # Read the point cloud

# 필드 존재 여부 확인
print("Has points:", pcd.has_points())
print("Has colors:", pcd.has_colors())
print("Has normals:", pcd.has_normals())

# 포인트 데이터를 NumPy 배열로 변환
points_array = np.asarray(pcd.points)
colors_array = np.asarray(pcd.colors)

# 모든 정보 다 출력해보기
print("Point Data Sample:")
header = "X, Y, Z"
if pcd.has_colors():
    header += ", R, G, B"
if pcd.has_normals():
    header += ", Nx, Ny, Nz"
print(header)

for i in range(min(10, len(points_array))):  # 최대 10개의 포인트만 출력
    # 기본 위치 데이터
    x, y, z = points_array[i]
    output = f"{x:.2f}, {y:.2f}, {z:.2f}"
    
    # 색상 데이터 (RGB)
    if pcd.has_colors():
        r, g, b = colors_array[i] * 255  # 색상 정보를 0-255 범위로 출력하기 위해 255를 곱함
        output += f", {int(r)}, {int(g)}, {int(b)}"
    
    # 정규 벡터 데이터 (Normals)
    if pcd.has_normals():
        nx, ny, nz = pcd.normals[i]
        output += f", {nx:.2f}, {ny:.2f}, {nz:.2f}"
    
    print(output)

# 포인트 클라우드 시각화
o3d.visualization.draw_geometries([pcd]) 
