import numpy as np
import laspy
import open3d as o3d

def pcd2las(file,save_path):
    txt = np.loadtxt(file)
    points = txt[:,0:3]
    inten = txt[:,3:4]

    #获取强度属性
    intensity_min = inten.min()
    intensity_max = inten.max()
    
    a = np.size(inten)
    inten2 = np.zeros(shape=(a,1))
    
    for i in range(a):
        intensity = inten[i,0]
        intensity_normalized = (intensity - intensity_min) * (65535 / (intensity_max - intensity_min))
        inten2[i,0] = int(intensity_normalized)

    
    
    txtout = np.concatenate((points,inten2),axis=1)
    
    np.savetxt(save_path,txtout,fmt='%.08f,%.08f,%.08f,%d',delimiter=',')
    
file = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/0_fullmap_ds.txt'
save_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/0_fullmap_ds_it.txt'
pcd2las(file,save_path)
