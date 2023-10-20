import os
import open3d as o3d
from shutil import copyfile
import numpy as np

# labelpath= '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/1_labels/'
# pcdpath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_pcd/'
# outpath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/tmp/'

# files = os.listdir(labelpath)
# names = []
# for file in files:
#     name, _ = file.split('.')
#     # names.append(name)
#     pcdfile = pcdpath + name + '.pcd'
#     outfile = outpath + name + '.pcd'
    
    
#     copyfile(pcdfile, outfile)      
    
# names

# pcd = o3d.io.read_point_cloud("/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_txt/000079.pcd")

# o3d.io.write_point_cloud("/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_txt/000079_c.pcd", pcd, True)

from pypcd import pypcd

pc = pypcd.PointCloud.from_path('/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/0_point_pcd/000079.pcd')
tmp_array = pc.pc_data.view(np.float64).reshape(pc.pc_data.shape+(-1,))  # numpy.ndarray (N,4)
# a = pc.pc_data.shape
# b = pc.pc_data.view()
# tmp_array = pc.pc_data.view().reshape(pc.pc_data.shape[0],4)

pc_array =np.zeros((pc.pc_data.shape[0],4))
pc_array[:,0:3] = np.array(tmp_array[:,0:3])
pc_array[:,3:4] = np.array(tmp_array[:,3:4])

pc