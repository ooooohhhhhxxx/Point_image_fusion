import os
import random
from PIL import Image
import pandas as pd

street_imgdir = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\streetview\compressed/'


img_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\only_sign\train_sign/'

img_save_path = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\streetview\mixed/'

num = 39209

files = os.listdir(img_path)

def random_get_file(dir):
    file_names = []
    for parent, dirnames, filenames in os.walk(dir):
        file_names = filenames
    x = random.randint(0, len(file_names)-1)
    return file_names[x]

for i in range(num):
    
    p_x = random.randint(200,1800)
    p_y = random.randint(500,1300)
    
    #image
    img1 = Image.open(street_imgdir + random_get_file(street_imgdir))
    img2 = Image.open(street_imgdir + random_get_file(street_imgdir))
    img = Image.blend(img1, img2, 0.5)
    img_savepath = img_save_path + str(i) + '.jpg'
    img.save(img_savepath)
    
    
    print(i,' done')






