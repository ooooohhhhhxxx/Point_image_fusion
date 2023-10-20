import open3d as o3d
import numpy as np
import os

def get_file(path):
    files = os.listdir(path)
    names = []
    for file in files:
        name, _ = file.split('.')
        names.append(name)
    return names

if __name__ == '__main__':
    txtpath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/5_full_cluster/'
    savepath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/6_center.txt'
    
    filenames = get_file(txtpath)
    center_list = []
    for filename in filenames:
        path = txtpath + filename + '.txt'
        
        try:
            txt = np.loadtxt(path)
            points = txt[:,0:3]
            ids = txt[:,4:5]
        except:
            pass
        
        
        # txt = np.loadtxt(path)
        # points = txt[:,0:3]
        # ids = txt[:,4:5]
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        center = pcd.get_center()
        center = np.array(center)
        id = ids[0]
        id = np.array(id)
        center = np.concatenate((center,id),axis=0).reshape(1,4)
        center = center.tolist()
        
        center_list.extend(center)
        
        # np.savetxt(savepath,np.array(center_list))
        
        # center = np.mean(points, axis=0)
        # center = np.array(center)
        # id = ids[0]
        # id = np.array(id)
        # center = np.concatenate((center,id),axis=0).reshape(1,4)
        # center = center.tolist()
        
        # center_list.extend(center)
    np.savetxt(savepath,np.array(center_list),fmt='%.08f')
        
    