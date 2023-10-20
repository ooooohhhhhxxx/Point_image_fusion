import open3d as o3d
import numpy as np


def euclidean_cluster(cloud, tolerance=0.2, min_cluster_size=100, max_cluster_size=1000):
    """
    欧式聚类
    :param cloud:输入点云
    :param tolerance: 设置近邻搜索的搜索半径（也即两个不同聚类团点之间的最小欧氏距离）
    :param min_cluster_size:设置一个聚类需要的最少的点数目
    :param max_cluster_size:设置一个聚类需要的最大点数目
    :return:聚类个数
    """

    kdtree = o3d.geometry.KDTreeFlann(cloud)  # 对点云建立kd树索引

    num_points = len(cloud.points)
    processed = [-1] * num_points  # 定义所需变量
    clusters = []  # 初始化聚类
    # 遍历各点
    for idx in range(num_points):
        if processed[idx] == 1:  # 如果该点已经处理则跳过
            continue
        seed_queue = []  # 定义一个种子队列
        sq_idx = 0
        seed_queue.append(idx)  # 加入一个种子点
        processed[idx] = 1

        while sq_idx < len(seed_queue):

            k, nn_indices, _ = kdtree.search_radius_vector_3d(cloud.points[seed_queue[sq_idx]], tolerance)

            if k == 1:  # k=1表示该种子点没有近邻点
                sq_idx += 1
                continue
            for j in range(k):

                if nn_indices[j] == num_points or processed[nn_indices[j]] == 1:
                    continue  # 种子点的近邻点中如果已经处理就跳出此次循环继续
                seed_queue.append(nn_indices[j])
                processed[nn_indices[j]] = 1

            sq_idx += 1

        if max_cluster_size > len(seed_queue) > min_cluster_size:
            clusters.append(seed_queue)

    return clusters


if __name__ == '__main__':
    
    savepath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/5_full_cluster/'
    # --------------------------加载点云数据------------------------------
    txt = np.loadtxt('/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/4_scalefilter.txt')
    points = txt[:,0:3]
    inten = txt[:,3:4]
    ids = txt[:,4:5]
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    # ---------------------------欧式聚类--------------------------------
    ec = euclidean_cluster(pcd, tolerance=0.5, min_cluster_size=5, max_cluster_size=100000)
    # -------------------------聚类结果分类保存---------------------------

    for i in range(len(ec)):
        ind = ec[i]
        clusters_cloud = pcd.select_by_index(ind)
        points_c = np.asarray(clusters_cloud.points)
        
        inten_c = []
        ids_c = []
        for j in ind:
            i_t = inten[j, 0]
            id_t = ids[j,0]
            inten_c.append(i_t)
            ids_c.append(id_t)
        inten_c = np.array(inten_c)
        inten_c = inten_c[:,np.newaxis]
        ids_c = np.array(ids_c)
        ids_c = ids_c[:,np.newaxis]
            
        cloud_c = np.concatenate((points_c,inten_c,ids_c),axis=1)
        
        
        
        file_name = savepath + "euclidean_cluster" + str(i + 1) + ".txt"
        np.savetxt(file_name,cloud_c)