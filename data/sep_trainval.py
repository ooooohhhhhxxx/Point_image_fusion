import os


def get_filelist(dataDir, outpath):
    files = os.listdir(dataDir)
    txt = open(outpath, 'w')
    for file in files:
        path = os.path.join(dataDir, file)
        path = path + '\n'
        txt.write(str(path))


datadir = '/Users/jinxuanchen/Desktop/test/dataset/images/val/'
outpath = '/Users/jinxuanchen/Desktop/test/dataset/val.txt'
get_filelist(datadir, outpath)
