# import open3d as o3d
# import numpy as np
# import os

# def read_point_cloud_bin(bin_path):
#     """
#     Read point cloud in bin format

#     Parameters
#     ----------
#     bin_path: str
#         Input path of Oxford point cloud bin

#     Returns
#     ----------

#     """
#     data = np.fromfile(bin_path, dtype=np.float32)

#     # format:
#     N, D = data.shape[0]// 6, 6
#     point_cloud_with_normal = np.reshape(data, (N, D))

#     point_cloud = o3d.geometry.PointCloud()
#     point_cloud.points = o3d.utility.Vector3dVector(point_cloud_with_normal[:, 0:3])
#     point_cloud.normals = o3d.utility.Vector3dVector(point_cloud_with_normal[:, 3:6])

#     return point_cloud


# def main(bin_path,pcd_path):
#     file_list = os.listdir(bin_path)
#     for onefile in file_list:
#         file_path = bin_path + onefile
#         filename,_ = onefile.split(".")
#         savepath = pcd_path + filename + '.pcd'
#         pc = read_point_cloud_bin(file_path)
#         o3d.io.write_point_cloud(savepath,pc)
#         print(filename,' done!')


# bin_path = '/Users/jinxuanchen/Downloads/2011_09_26-5/2011_09_26_drive_0029_sync/velodyne_points/data/'
# pcd_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/fusion_test/pcd/split/'
# main(bin_path,pcd_path)

import os
import numpy as np
import struct
import open3d as o3d


def read_bin_velodyne(path):
    pc_list = []
    with open(path, 'rb') as f:
        content = f.read()
        pc_iter = struct.iter_unpack('ffff', content)
        for idx, point in enumerate(pc_iter):
            pc_list.append([point[0], point[1], point[2],point[3]])
    return np.asarray(pc_list, dtype=np.float32)


def main(bin_path, pcd_path):
    files = os.listdir(bin_path)
    file_number = len(files)

    pcd = o3d.open3d.geometry.PointCloud()

    for i in range(file_number):
        path = os.path.join(bin_path, files[i])
        name,_ = files[i].split('.')
        savepath = pcd_path + name + '.txt'
        example = read_bin_velodyne(path)
        a = example[:,2]
        # # From numpy to Open3D
        # pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.open3d.utility.Vector3dVector(example)
        # pcd.normals = o3d.open3d.utility.DoubleVector(example[:3])
        # # o3d.io.write_point_cloud(savepath,pcd)
    
        # o3d.open3d.visualization.draw_geometries([pcd],point_show_normal=True )
        np.savetxt(savepath,example,fmt='%.08f')
        print(name,' done!')

if __name__ == "__main__":
    bin_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/fusion_test/pcd/378/pc/'
    pcd_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/fusion_test/pcd/378/'
    main(bin_path, pcd_path)
