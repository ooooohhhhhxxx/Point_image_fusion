import os
import random
from PIL import Image
import pandas as pd

street_imgdir = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\streetview\compressed/'


label_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\labels\onlysign\val/'
img_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\only_sign\val/'

img_save_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\val/'
label_save_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\labels\val/'

files = os.listdir(img_path)

def random_get_file(dir):
    file_names = []
    for parent, dirnames, filenames in os.walk(dir):
        file_names = filenames
    x = random.randint(0, len(file_names)-1)
    return file_names[x]

for file in files:
    img_p = img_path + file
    name,_  = file.split('.')
    label_p = label_path + name + '.txt'
    
    p_x = random.randint(200,1800)
    p_y = random.randint(500,1300)
    
    #image
    sign = Image.open(img_p)
    img1 = Image.open(street_imgdir + random_get_file(street_imgdir))
    img2 = Image.open(street_imgdir + random_get_file(street_imgdir))
    img = Image.blend(img1, img2, 0.5)
    img.paste(sign,(p_x,p_y))
    img_savepath = img_save_path + name + '.jpg'
    img.save(img_savepath,quality=40)
    
    #label
    o_w, o_h = sign.size
    label = pd.read_csv(label_p,header=None,sep=' ')
    
    id, x, y, w, h = label[0][0], label[1][0]*o_w, label[2][0]*o_h, label[3][0]*o_w, label[4][0]*o_h
    # x1 = x - w/2
    # y1 = y - h/2 
    # x2 = x + w/2
    # y2 = y + h/2
    # x_n = ((x2 - x1)/2 + p_x)/2048 
    # y_n = ((y2 - y1)/2 + p_y)/2048
    x_n = (x+p_x)/2048
    y_n = (y+p_y)/2048
    w_n = w /2048 
    h_n = h /2048
    
    label_savepath = label_save_path + name + '.txt'
    with open(label_savepath,'w') as f:
        f.write(str(id) + ' ' + str(x_n) + ' ' + str(y_n) + ' ' + str(w_n) + ' ' + str(h_n))
    
    print(name,' done')






