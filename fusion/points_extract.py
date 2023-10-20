import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import os
import open3d as o3d


imgpath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/image_2/'
labelpath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/1_labels/'
binarypath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/velodyne/'
# point_out_pcd = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/00/0_out/2_out_pcd/'
point_out_txt = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/2_out_txt/'
parameter_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/'

points_pose_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/0_point_pcd/'

box_enlarge = 15


def get_file():
    files = os.listdir(labelpath)
    names = []
    for file in files:
        name, _ = file.split('.')
        names.append(name)
    return names

# 获取内外参


# def get_parameter():
#     files = os.listdir(parameter_path)

#     for file in files:
#         if file == 'calib_cam_to_cam.txt':
#             with open(parameter_path+file) as file:
#                 for line in file:
#                     if line[0:9] == 'R_rect_00':
#                         R0_rect = np.matrix(line[10:]).reshape(3, 3)
#                         R0_rect = np.insert(
#                             R0_rect, 3, values=[0, 0, 0], axis=0)
#                         R0_rect = np.insert(R0_rect, 3, values=[
#                                             0, 0, 0, 1], axis=1)
#                     if line[0:9] == 'P_rect_02':
#                         P2 = np.matrix(line[10:]).reshape(3, 4)
#         if file == 'calib_velo_to_cam.txt':
#             with open(parameter_path+file) as file:
#                 for line in file:
#                     if line[0:1] == 'R':
#                         R = np.matrix(line[2:]).reshape(3, 3)
#                     if line[0:1] == 'T':
#                         T = np.matrix(line[2:]).reshape(3, 1)
#         Tr_velo_to_cam = np.hstack((R, T))
#         Tr_velo_to_cam = np.insert(
#             Tr_velo_to_cam, 3, values=[0, 0, 0, 1], axis=0)

#     return Tr_velo_to_cam, R0_rect, P2

def get_parameter():
    files = os.listdir(parameter_path)

    for file in files:
        if file == 'calib.txt':
            with open(parameter_path+file) as file:
                for line in file:
                    if line[0:2] == 'P2':
                        P2 = np.matrix(line[3:]).reshape(3, 4)
                    if line[0:2] == 'Tr':
                        Tr_velo_to_cam = np.matrix(line[3:]).reshape(3, 4)
                        Tr_velo_to_cam = np.insert(Tr_velo_to_cam, 3, values=[0, 0, 0, 1], axis=0)

    return Tr_velo_to_cam, P2



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
    index1 = np.delete(index, np.where(velo[0, :] < 0), axis=1)

    # path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/2011_09_26_drive_0096_sync/test/'+filename +'.txt'
    # np.savetxt(path, points, fmt="%.8f")
    return points, velo1, intensity, index1

# def get_cam(velo, index):

#     Tr_velo_to_cam, R0_rect, P2 = get_parameter()

#     cam = P2 * R0_rect * Tr_velo_to_cam * velo
#     cam1 = np.delete(cam, np.where(cam[2, :] < 0)[1], axis=1)
#     index_cam1 = np.delete(index, np.where(cam[2, :] < 0)[1], axis=1)

#     # get u,v,z
#     cam1[:2] /= cam1[2, :]

#     return cam1, index_cam1


def get_cam(velo, index):

    Tr_velo_to_cam, P2 = get_parameter()

    cam = P2  * Tr_velo_to_cam * velo
    cam1 = np.delete(cam, np.where(cam[2, :] < 0)[1], axis=1)
    index_cam1 = np.delete(index, np.where(cam[2, :] < 0)[1], axis=1)

    # get u,v,z
    cam1[:2] /= cam1[2, :]

    return cam1, index_cam1


def get_image(filename):
    path = imgpath +filename + ".png"
    img = mpimg.imread(path)
    IMG_H, IMG_W, _ = img.shape

    return IMG_H, IMG_W


def filter_points(cam, index_cam, filename):
    u, v, z = cam
    IMG_H, IMG_W = get_image(filename)
    u_out = np.logical_or(u < 0, u > IMG_W)
    v_out = np.logical_or(v < 0, v > IMG_H)
    outlier = np.logical_or(u_out, v_out)
    cam1 = np.delete(cam, np.where(outlier), axis=1)
    index_cam1 = np.delete(index_cam, np.where(outlier), axis=1)

    # path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/2011_09_26_drive_0096_sync/test/'+filename +'.txt'
    # np.savetxt(path,cam.T, fmt="%.8f")
    return cam1, index_cam1


def get_labels(filename):
    path = labelpath + filename + '.txt'
    label = pd.read_csv(path, header=None, sep=' ')

    return label


def get_pointsinbox(filename, cam, index_cam):
    u, v, z = cam

    # img_path = imgpath + filename + '.png'
    # points_inbox = Image.open(img_path)
    # pinb = ImageDraw.ImageDraw(points_inbox)
    _, n = u.shape
    # u_2d = []
    # v_2d = []
    # z_2d = []
    index_inbox = []
    ids = []

    label = get_labels(filename)

    for i in range(len(label[0])):
        box_lx = int(label[1][i]*1242-label[3][i]*1242/2 - box_enlarge)
        box_ly = int(label[2][i]*375-label[4][i]*375/2-box_enlarge)
        box_rx = int(label[1][i]*1242+label[3][i]*1242/2+box_enlarge)
        box_ry = int(label[2][i]*375+label[4][i]*375/2+box_enlarge)
        id = label[0][i]

        for j in range(0, n):
            if box_lx < u[0, j] < box_rx and box_ly < v[0, j] < box_ry:
                # xinb_2d = (u[0, j])
                # yinb_2d = (v[0, j])
                # zinb_2d = (z[0, j])
                # u_2d.append(xinb_2d)
                # v_2d.append(yinb_2d)
                # z_2d.append(zinb_2d)
                index_inbox.append(index_cam[0, j])
                ids.append(id)
                
    #             pinb.point((int(xinb_2d), int(yinb_2d)), (255, 0, 0))

    # saveimg_path = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/2011_09_26_drive_0096_sync/test_img/' + filename + '.jpg'
    # points_inbox.save(saveimg_path)
    return index_inbox,ids


def get_points(index_inbox, points, intensity,ids):
    x = []
    y = []
    z = []
    inten = []
    id = []

    # for i in index_inbox:
    #     x_t = points[int(i), 0]
    #     y_t = points[int(i), 1]
    #     z_t = points[int(i), 2]
    #     i_t = intensity[0, int(i)]
    #     # id_t = ids[0,int(i)]
    #     x.append(x_t)
    #     y.append(y_t)
    #     z.append(z_t)
    #     inten.append(i_t)
    #     # id.append(id_t)
        
    for i in range(len(index_inbox)):
        x_t = points[index_inbox[i], 0]
        y_t = points[index_inbox[i], 1]
        z_t = points[index_inbox[i], 2]
        i_t = intensity[0, index_inbox[i]]
        id_t = ids[i]
        x.append(x_t)
        y.append(y_t)
        z.append(z_t)
        inten.append(i_t)
        id.append(id_t)

    return x, y, z, inten, id

def read_points_pose(filename):
    path = points_pose_path + filename + ".pcd"
    
    # scan = np.loadtxt(path)
    # points = scan[:, 0:3]  # lidar xyz (front, left, up)
    # intensity = scan[:, 3:4].T
    
    # # points = scan[:, 0:3]  # lidar xyz (front, left, up)
    # # intensity = scan[:, 3:4].T
    
    from pypcd import pypcd

    pc = pypcd.PointCloud.from_path(path)
    tmp_array = pc.pc_data.view(np.float64).reshape(pc.pc_data.shape+(-1,))  # numpy.ndarray (N,4)

    scan =np.zeros((pc.pc_data.shape[0],4))
    scan[:,0:3] = np.array(tmp_array[:,0:3])
    scan[:,3:4] = np.array(tmp_array[:,3:4])
    
    points = scan[:, 0:3]  # lidar xyz (front, left, up)
    intensity = scan[:, 3:4].T
    
    return points,intensity

def points_save(filename, x, y, z, inten,id):
    
    
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    inten = np.array(inten)
    
    s= x.shape
    s = s[0]
    # ids = np.full((s,),id,dtype=int)
    ids = np.array(id)
    
    #txt保存
    txt= np.vstack((x,y,z,inten,ids)).T
    
    for i in range(len(x)):
        if x[i] != 0:
            path_txt = point_out_txt + filename + '.txt'
            np.savetxt(path_txt, txt,fmt='%.08f')
    
    
    #只要xyzi
    # points = np.vstack((x,y,z)).T
    # pcdt = o3d.t.geometry.PointCloud()
    # pcdt.point['positions'] = o3d.core.Tensor(points)
    # pcdt.point['intensities'] = o3d.core.Tensor(inten.reshape(-1,1))

    # path = point_out_pcd + filename + '.pcd'
    # o3d.t.io.write_point_cloud(path, pcdt,write_ascii = True) 


if __name__ == "__main__":

    for filename in get_file():
        print(filename + ' is  reading')
        points, velo, intensity, index = read_bin(filename)
        cam, index_cam = get_cam(velo, index)
        cam1, index_cam = filter_points(cam, index_cam, filename)

        # labels = get_labels(filename)

        index_inbox ,ids = get_pointsinbox(filename, cam1, index_cam)
        print('calculating index')

        points_pose, inten_poes = read_points_pose(filename)
        # x, y, z, inten = get_points(index_inbox, points, intensity)
        x, y, z, inten ,id= get_points(index_inbox, points_pose, inten_poes,ids)

        points_save(filename, x, y, z, inten,id)
        print(filename + ' is done')