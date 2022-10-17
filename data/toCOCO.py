import os
import pandas as pd
import numpy as np

image_width = 200
image_hight = 200


def traintoyolo(dataDir, outpath):
    labelDir = os.listdir(dataDir)
    # df = pd.DataFrame(
    #     columns=['Filename', 'Width', 'Roi.X1', 'Roi.Y1', 'Roi.X2', 'Roi.Y2', 'ClassId']
    # )
    df = pd.DataFrame()
    for label in labelDir:
        folder = dataDir + label + '/'
        onesavedir = outpath + label + '/'
        for file in os.listdir(folder):
            if file.endswith('.csv'):
                csvfile = os.path.join(folder, file)
        csv = pd.read_csv(csvfile)
        df = df.append(csv)
        csv_array = np.array(csv)
        for i in range(csv_array.shape[0]):
            csv_list = np.array(csv)[i, :].tolist()[0].split(";")
            filename, _ = csv_list[0].split('.')
            o_w = int(csv_list[1])
            o_h = int(csv_list[2])
            o_x1 = int(csv_list[3])
            o_y1 = int(csv_list[4])
            o_x2 = int(csv_list[5])
            o_y2 = int(csv_list[6])
            id = csv_list[7]
            x = str(((o_x2 - o_x1) / 2 + o_x1) / image_width)
            y = str(((o_y2 - o_y1) / 2 + o_y1) / image_hight)
            w = str(o_w / image_width)
            h = str(o_h / image_hight)
            data = {'id': id, 'x': x, 'y': y, 'w': w, 'h': h}
            out = pd.DataFrame(data, index=[0])
            path = outpath + label + '_' + filename + '.txt'
            out.to_csv(path, sep=' ', header=None, index=False)
            print(filename + ' done')
        print(label, ' done')
    df.to_csv('/Users/jinxuanchen/Desktop/test/11.csv')
    print('train done')


def valtoyolo(valpath, valsavepath):
    csv = pd.read_csv(valpath)
    csv_array = np.array(csv)
    for i in range(csv_array.shape[0]):
        csv_list = np.array(csv)[i, :].tolist()[0].split(";")
        filename, _ = csv_list[0].split('.')
        o_w = int(csv_list[1])
        o_h = int(csv_list[2])
        o_x1 = int(csv_list[3])
        o_y1 = int(csv_list[4])
        o_x2 = int(csv_list[5])
        o_y2 = int(csv_list[6])
        id = csv_list[7]
        x = str(((o_x2 - o_x1) / 2 + o_x1) / image_width)
        y = str(((o_y2 - o_y1) / 2 + o_y1) / image_hight)
        w = str(o_w / image_width)
        h = str(o_h / image_hight)
        data = {'id': id, 'x': x, 'y': y, 'w': w, 'h': h}
        out = pd.DataFrame(data, index=[0])
        path = valsavepath + filename + '.txt'
        out.to_csv(path, sep=' ', header=None, index=False)
        print(filename + ' done')
    print('val done')


if __name__ == '__main__':
    datapath = '/Users/jinxuanchen/Desktop/test/origin/GTSRB/Final_Training/Images/'
    savepath = '/Users/jinxuanchen/Desktop/test/label/train/'
    val_csv = '/Users/jinxuanchen/Desktop/test/origin/GT-final_test.csv'
    val_savepath = '/Users/jinxuanchen/Desktop/test/label/val/'
    traintoyolo(datapath, savepath)
    # valtoyolo(val_csv, val_savepath)