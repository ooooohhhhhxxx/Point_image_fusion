'''
WGS84的经纬度 转 UTM的x,y
'''
from pyproj import Transformer
 
 
# 参数1：WGS84地理坐标系统 对应 4326 
# 参数2：坐标系WKID 广州市 WGS_1984_UTM_Zone_49N 对应 32649
# 德国 UTM 32 号带  WGS_1984_UTM_Zone_32N
transformer = Transformer.from_crs("epsg:4326", "epsg:32632") 
 
# lat = 48.98254523586602
# lon = 8.39036610004500

lat = 48.987607723096
lon = 8.4697469732634
x, y = transformer.transform(lat, lon)
print("x:", x, "y:", y)

#x: 455394.37362745043 y: 5425694.4726226125
# x: 461206.410098871 y: 5426213.646902477
