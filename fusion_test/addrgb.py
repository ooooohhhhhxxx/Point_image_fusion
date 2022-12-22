import os
import pandas as pd
import random

txtpath = '/Users/jinxuanchen/Desktop/未命名文件夹/txt/'
file_outpath = '/Users/jinxuanchen/Desktop/未命名文件夹/1.txt'

files = os.listdir(txtpath)
all_df = pd.DataFrame()
for file in files:
    name, _ = file.split('.')
    filepath = txtpath + name + '.txt'

    df = pd.read_csv(filepath, sep=' ', header=None)

    df['3'] = random.randint(0, 256)
    df['4'] = random.randint(0, 256)
    df['5'] = random.randint(0, 256)

    all_df = pd.concat([all_df, df])
    print(name, ' read and add RGB done!')

all_df.to_csv(file_outpath, sep=' ', header=None, index=None )
