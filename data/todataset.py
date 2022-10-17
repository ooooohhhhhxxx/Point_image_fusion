import os
import shutil


def todataset(dataDir, outpath):
    labelDir = os.listdir(dataDir)
    for label in labelDir:
        labelfolder = dataDir + label + '/'
        objectDir = os.listdir(labelfolder)
        for ob in objectDir:
            path = os.path.join(labelfolder, ob)
            filename, _ = ob.split('.')
            newname = label + '_' + filename + '.png'
            newpath = os.path.join(outpath, newname)
            shutil.copyfile(path, newpath)
            print(filename, ' done')


trainDir = '/Users/jinxuanchen/Desktop/test/convert_png/train/'
outpath = '/Users/jinxuanchen/Desktop/test/image/train/'
todataset(trainDir, outpath)
