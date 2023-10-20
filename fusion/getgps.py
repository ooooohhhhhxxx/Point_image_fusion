import os
import pandas as pd

gpspath = '/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/oxts/data/'


files = os.listdir(gpspath)

df = pd.DataFrame(columns=['id','x','y','z'])
for file in files:
    name, _ = file.split('.')
    filepath = os.path.join(gpspath,file)
    df1 = pd.read_csv(filepath,sep=' ',header=None)
    id = name
    x = df1[0][0]
    y = df1[1][0]
    z = df1[2][0]
    
    df.loc[len(df.index)] = [id, x, y, z]

df.to_csv('/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/gps.txt',index=None)