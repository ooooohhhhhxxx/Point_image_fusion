import numpy as np
binarypath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_bin/'

def read_bin(filename):
    # path = binarypath +'0000000'+filename + ".bin"
    path = binarypath +filename + ".bin"
    scan = np.fromfile(path, dtype=np.float32).reshape((-1, 4))
    points = scan[:, 0:3]  # lidar xyz (front, left, up)
    intensity = scan[:, 3:4].T

    s, _ = points.shape
    index = np.arange(0, s).reshape(1, s)

    velo = np.insert(points, 3, 1, axis=1).T
    # _, s = velo.shape
    # index = np.arange(0, s).reshape(1, s)

    velo1 = np.delete(velo, np.where(velo[0, :] < 0), axis=1)
    

    # path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/2011_09_26_drive_0096_sync/test/'+filename +'.txt'
    # np.savetxt(path, points, fmt="%.8f")
    return points, velo1, intensity


points, velo1, intensity = read_bin('000000')

np.savetxt('/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_txt/000000.txt',points,fmt='%.07f')