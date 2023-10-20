# -*- coding:utf-8 -*-
"""使用获取的相机内外参数实现重投影"""

import open3d as o3d
import cv2
from PIL import Image
from pylab import *
import matplotlib.pyplot as plt

R = np.float64([[7.533745e-03, -9.999714e-01, -6.166020e-04],
                [1.480249e-02, 7.280733e-04, -9.998902e-01],
                [9.998621e-01, 7.523790e-03, 1.480755e-02]])
# 先做个转置
RT = np.transpose(R)
print(RT)

# 再求罗德里德斯变换
rvec = cv2.Rodrigues(RT)[0]
print(rvec)

# 读取pcd点云文件，保存为array数组
cloud = o3d.io.read_point_cloud(
    '/Users/jinxuanchen/Files_Local/Point_image_fusion/fusion_test/pcd/30_test/0000000030 - Cloud.pcd')  # 需要准备自己的pcd文件
cloud = np.asarray(cloud.points)  # 改变点云的数据类型

# 输入 projectpoints 函数的各项参数数值

# 经过矩阵转置，以及罗德里格斯变换得到的旋转矩阵
# rvec = np.float64([1.27379905, -1.17541056, 1.15989273])


# 经过排序修改后得到的平移矩阵
# tvec = np.float64([-0.07396497, 0.00705671, 0.06965965])
tvec = np.float64([-4.069766e-03, -7.631618e-02, -2.717806e-01])

# 相机内部参数
camera_matrix = np.float64([[6.0094877060462500e+02, 0,  3.0507696130640221e+02],
                            [0, 6.1174212550675293e+02,  2.5274596287337977e+02],
                            [0, 0, 1]])  # 相机内部参数
# camera_matrix = np.float64[0]
# 相机形变矩阵
distCoeffs = np.float64([2.3030430710414049e-01, -9.1560321189489913e-01,
                         1.0374975865423207e-02, -8.9662215743119679e-04, 1.3506515085650497e+00])
# distCoeffs = np.float64[0]

# 进行点云由3D到2D的转换
point_2d, _ = cv2.projectPoints(cloud, rvec, tvec, camera_matrix, distCoeffs)

print(point_2d)


# 重投影绘制在图像上
im = Image.open(
    '/Users/jinxuanchen/Files_Local/Point_image_fusion/fusion_test/pcd/30_test/0000000030.png')
x = []
y = []

m = -1
for point in point_2d:
    m = m+1
    x_2d = point[0][0]
    y_2d = point[0][1]

    if 0 <= x_2d <= 1242 and 0 <= y_2d <= 375:
        x.append(x_2d)
        y.append(y_2d)

x = np.array(x)
y = np.array(y)
plt.scatter(x, y, s=1)
plt.imshow(im)
plt.show()
