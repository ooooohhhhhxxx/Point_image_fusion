import os
import PIL
import numpy as np
import pandas as pd
from PIL import Image

train_path = (
    r'C:\Users\JinXuanchen\Downloads\GTSRB_Final_Training_Images\GTSRB\Final_Training\Images/'
)

test_path = r'C:\Users\JinXuanchen\Downloads\GTSRB_Final_Test_Images\GTSRB\Final_Test\Images/'

train_outpath = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\train/'
test_outpath = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\val/'


def convertTrainData(dataDir, saveDir):
    '''
    训练数据集转化处理
    '''
    labelDir = os.listdir(dataDir)
    for label in labelDir:
        oneDir = dataDir + label + '/'
        oneSaveDir = saveDir + label + '/'
        if not os.path.exists(oneSaveDir):
            os.makedirs(oneSaveDir)
        for one_file in os.listdir(oneDir):
            if one_file.endswith(".csv"):
                csvFile = os.path.join(oneDir, one_file)
        csv_data = pd.read_csv(csvFile)
        csv_data_array = np.array(csv_data)
        for i in range(csv_data_array.shape[0]):
            csv_data_list = np.array(csv_data)[i, :].tolist()[0].split(";")
            one_ppm = os.path.join(oneDir, csv_data_list[0])
            img = Image.open(one_ppm)
            # box = [
            #     int(csv_data_list[3]),
            #     int(csv_data_list[4]),
            #     int(csv_data_list[5]),
            #     int(csv_data_list[6]),
            # ]
            # img = img.crop(box)

            bg = Image.new('RGB', (200, 200), (0, 0, 0))
            bg.paste(img, (0, 0))

            filename, _ = csv_data_list[0].split(".")
            one_save_path = oneSaveDir + filename + '.png'
            # oneSaveDir + '' + '.png'
            bg.save(one_save_path)


def convertTestData(dataDir, saveDir):
    '''
    测试数据集转化处理
    '''
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    file_list = os.listdir(dataDir)
    for one_file in file_list:
        if one_file.endswith(".csv"):
            csvFile = os.path.join(dataDir, one_file)
    csv_data = pd.read_csv(csvFile)
    csv_data_array = np.array(csv_data)
    for i in range(csv_data_array.shape[0]):
        csv_data_list = np.array(csv_data)[i, :].tolist()[0].split(";")
        one_ppm = os.path.join(dataDir, csv_data_list[0])
        img = Image.open(one_ppm)
        # box = [
        #     int(csv_data_list[3]),
        #     int(csv_data_list[4]),
        #     int(csv_data_list[5]),
        #     int(csv_data_list[6]),
        # ]
        # img = img.crop(box)

        bg = Image.new('RGB', (200, 200), (0, 0, 0))
        bg.paste(img, (0, 0))

        filename, _ = csv_data_list[0].split(".")
        one_save_path = saveDir + filename + '.png'
        bg.save(one_save_path)


convertTrainData(dataDir=train_path, saveDir=train_outpath)
convertTestData(dataDir=test_path, saveDir=test_outpath)
