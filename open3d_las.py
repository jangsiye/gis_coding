
# .las 파일을 열어서 포인트 클라우드로 변환하는 예제

# laspy 라이브러리를 사용하여 .las 파일을 열고, open3d를 사용하여 포인트 클라우드로 변환
# laspy는 las 파일을 읽고 쓰는 라이브러리로, las 파일의 헤더 정보와 포인트 데이터를 쉽게 읽고 쓸 수 있음
# open3d는 3D 데이터를 시각화하고 처리하는 라이브러리로, 포인트 클라우드 데이터를 쉽게 시각화할 수 있음

import numpy as np
import open3d as o3d

file_name = 'D:/ways1_datas/강릉시/강릉시/강릉시/LAS/2022-APR-11_202204110000_LGU_GANGNEUNG_1/2022_202204110334_S35.las'

# gpt에게 물어본 일반적인 las 파일 여는법
import laspy

las = laspy.read(file_name)
header = las.header
print(header)
print(f"Version: {header.version}")
print(f"Point Format: {header.point_format}")
print(f"Number of Points: {header.point_count}")

# 몇 개의 포인트 데이터 예제 출력
print("\nPoint Data Sample:")
print("X, Y, Z, Intensity, Return Number, Number of Returns, Scan Direction, Edge of Flight Line, Classification, Scan Angle Rank, User Data, Point Source ID, GPS Time")
for point in las.points[:10]:  # 처음 10개 포인트만 출력
    # 좌표 정보는 파일 헤더에 저장된 스케일 및 오프셋을 사용하여 실제 좌표로 변환
    x = point.X * header.scales[0] + header.offsets[0]
    y = point.Y * header.scales[1] + header.offsets[1]
    z = point.Z * header.scales[2] + header.offsets[2]
    print(f"{x:.2f}, {y:.2f}, {z:.2f}, {point.intensity}, {point.return_number}, {point.number_of_returns}, {point.scan_direction_flag}, {point.edge_of_flight_line}, {point.classification}, {point.scan_angle_rank}, {point.user_data}, {point.point_source_id}, {point.gps_time}")

# SubFieldView 객체 : laspy에서 각 필드의 값을 효율적으로 처리하기 위해 사용되는 컨테이너

# 반환 펄스 수(Return Number): 단일 레이저 펄스가 여러 객체에 반사되어 여러 개의 반환 신호를 생성할 때, 해당 포인트가 몇 번째로 반환된 것인지를 나타냄. ex) 1 : 첫 번째 반환 신호임
# 반환 펄스의 총 수(Number of Returns): 단일 레이저 펄스에 대해 총 몇 개의 반환 신호가 있는지를 나타냄. ex) 1 : 하나의 반환만 있음
# 스캔 방향 플래그(Scan Direction Flag): 레이저가 스캔할 때의 방향. 0은 일반적으로 한 방향(예: 왼쪽에서 오른쪽), 1은 반대 방향을 의미
# 비행선 가장자리 플래그(Edge of Flight Line): 해당 포인트가 비행 경로의 가장자리에 있는지를 나타냄. 0은 가장자리가 아님을, 1은 가장자리임을 의미
# 분류(Classification): 포인트가 속하는 객체의 유형(예: 지면, 식생, 건물 등)을 나타냄. 1이면 일반적으로 '지면' 또는 'Ground'을 의미

# 라이더 분류(Classification) 코드 정보 출력
classification_codes = {
    0: "Unassigned",
    1: "Ground",
    2: "Low Vegetation",
    3: "Medium Vegetation",
    4: "High Vegetation",
    5: "Building",
    6: "Low Point (noise)",
    7: "High Point (noise)",
    8: "Water",
    9: "Rail",
    10: "Road Surface",
    11: "Reserved",
    12: "Power Line",
    13: "Wire – Conductor",
    14: "Transmission Tower",
    15: "Wire-Structure Connector",
    # 추가 분류 필요 시 확장 가능
}

# 분류 정보를 문자열로 매핑하여 출력
for point in las.points[:10]:
    classification = classification_codes.get(point.classification.array, "Unknown")
    print(f"Classification: {classification}")

# open3d 포인트 클라우드 객체로 변환

# 포인트 데이터를 numpy 배열로 추출
points = np.vstack((las.x, las.y, las.z)).transpose()

# open3d 포인트 클라우드 객체 생성
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# 포인트 클라우드 시각화
o3d.visualization.draw_geometries([pcd])

