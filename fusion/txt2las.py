from whitebox import WhiteboxTools

wbt = WhiteboxTools()

wbt.set_working_dir('/Users/jinxuanchen/Files_Local/Point_image_fusion/kittidata/odometry/sequences/02/0_out/')

wbt.ascii_to_las(inputs = '0_fullmap_ds_it.txt',pattern='x,y,z,i',proj='32632')

