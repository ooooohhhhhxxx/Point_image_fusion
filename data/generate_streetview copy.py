import os
import random
from PIL import Image
import pandas as pd
import cv2

street_imgdir = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\streetview\compressed/'


label_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\labels\onlysign\val/'
img_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\only_sign\val/'

img_save_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\val/'
label_save_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\labels\val/'


files = os.listdir(img_path)
files_df = pd.DataFrame(files)
length = len(files_df)
a = range(5)

def random_get_file(dir):
    file_names = []
    for parent, dirnames, filenames in os.walk(dir):
        file_names = filenames
    x = random.randint(0, len(file_names)-1)
    return file_names[x]

i = 0
while(i < length):
    sum = random.randint(1,4)
    
    img1 = cv2.imread((street_imgdir + random_get_file(street_imgdir)))
    img2 = cv2.imread(street_imgdir + random_get_file(street_imgdir))
    img = cv2.addWeighted(img1, 0.7,img2, 0.5, 0)
    label_n = pd.DataFrame()
    
    for j in range(sum):
        file_num = i + j
        file = files_df[0][file_num]
        img_p = img_path + file
        name,_  = file.split('.')
        label_p = label_path + name + '.txt'
        
        p_x = random.randint(200,1800)
        p_y = random.randint(300,1600)
        
        sign = cv2.imread(img_p)
        rows,cols,channels = sign.shape
        img[p_y:p_y + rows, p_x:  p_x + cols] = sign
        
        
        size = sign.shape
        o_w = size[0]
        o_h = size[1]
        
        label = pd.read_csv(label_p,header=None,sep=' ')
        id, x, y, w, h = label[0][0], label[1][0]*o_w, label[2][0]*o_h, label[3][0]*o_w, label[4][0]*o_h
        x_n = (x+p_x)/2048
        y_n = (y+p_y)/2048
        w_n = w /2048 
        h_n = h /2048
        
        label_savepath = label_save_path + str(i) + '.txt'
        with open(label_savepath,'a') as f:
            f.write(str(id) + ' ' + str(x_n) + ' ' + str(y_n) + ' ' + str(w_n) + ' ' + str(h_n) +'\n')
    
    img_savepath = img_save_path + str(i) + '.jpg'
    cv2.imwrite(img_savepath,img,[int(cv2.IMWRITE_JPEG_QUALITY),50])
    i += sum
    # print(name, ' done')







