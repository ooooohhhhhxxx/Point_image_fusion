import os
import cv2
from PIL import Image
from PIL import ImageDraw
import pandas as pd


label_path = '/Users/jinxuanchen/Downloads/tt100k_2021/tt100K/out/label/'
img_path = '/Users/jinxuanchen/Downloads/tt100k_2021/tt100K/out/image/'
img_save_path = '/Users/jinxuanchen/Downloads/tt100k_2021/tt100K/out/image_withcover/'


names = os.listdir(label_path)
for name in names:
    name = name.split('.')[0]
    label_p = label_path + name + '.txt'
    img_p = img_path + name + '.jpg'
    try:   
        img = Image.open(img_p)
        label = pd.read_csv(label_p, header=None,sep=' ')
        a = ImageDraw.ImageDraw(img)
        for i in range(len(label[0])):
            a.rectangle(((label[0][i],label[1][i]),(label[2][i],label[3][i])),fill='black')
        save_path = img_save_path + name + '.jpg'
        img.save(save_path)
    except:
        continue
    