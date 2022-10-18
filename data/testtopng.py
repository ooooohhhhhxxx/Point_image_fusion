import os
import PIL
import numpy as np
import pandas as pd
from PIL import Image


test_path = r'C:\Users\JinXuanchen\Downloads\FullIJCNN2013\FullIJCNN2013\test_full/'

test_outpath = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\test/'


def convertTestData(dataDir, saveDir):
    '''
    测试数据集转化处理
    '''
    files = os.listdir(dataDir)
    for file in files:
        name,_ = file.split('.')
        path = os.path.join(dataDir,file)
        img = Image.open(path)
        savepath = saveDir + name +'.png'
        img.save(savepath)


convertTestData(dataDir=test_path, saveDir=test_outpath)
