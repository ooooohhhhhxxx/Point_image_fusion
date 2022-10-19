import os


def get_filelist(dataDir, outpath):
    files = os.listdir(dataDir)
    txt = open(outpath, 'w')
    for file in files:
        path = os.path.join(dataDir, file)
        path = path + '\n'
        txt.write(str(path))


datadir = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\images\val'
outpath = r'C:\Users\JinXuanchen\Documents\Point_image_fusion\datasets\val.txt'
get_filelist(datadir, outpath)
a=1