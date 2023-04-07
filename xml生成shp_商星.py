import glob
import os
import re
from xml.etree import ElementTree as ET

import pandas as pd
from osgeo import ogr, osr, gdal


def huoquInfo(path_base):
    if (os.path.exists(path_base)):
        f = glob.glob(path_base + '/SV*.xml')
    df = pd.DataFrame()
    excel_data = [['子订单号', '卫星', '成像开始时间', '景号', '产品号', '视角',
                   '左上角经度', '左上角纬度', '右上角经度', '右上角纬度', '右下角经度', '右下角纬度', '左下角经度',
                   '左下角纬度', '云量']]
    c = 1  # 行
    for file in f:
        # print (file)
        test = []
        # 打开文件
        dom = ET.parse(file)
        # 文档根元素
        root = dom.getroot()
        # 四角点坐标
        TopLeftLongitude = round(float(root.find('TopLeftLongitude').text), 5)
        TopLeftLatitude = round(float(root.find('TopLeftLatitude').text), 5)
        TopRightLongitude = round(float(root.find('TopRightLongitude').text), 5)
        TopRightLatitude = round(float(root.find('TopRightLatitude').text), 5)
        BottomRightLongitude = round(float(root.find('BottomRightLongitude').text), 5)
        BottomRightLatitude = round(float(root.find('BottomRightLatitude').text), 5)
        BottomLeftLongitude = round(float(root.find('BottomLeftLongitude').text), 5)
        BottomLeftLatitude = round(float(root.find('BottomLeftLatitude').text), 5)
        try:
            test.append(''.join(re.findall('\d', root.find('DataArchiveFile').text.split('_')[3])))
        except:
            test.append(''.join(re.findall('\d', root.find('DataFile').text.split('_')[3])))
        test.append(root.find('SatelliteID').text)
        test.append(root.find('StartTime').text.split(' ')[0].replace('-', ''))
        test.append(root.find('SceneID').text)
        test.append(int(root.find('ProductID').text))
        test.append(int(float(root.find('ViewAngle').text)))
        test.append(TopLeftLongitude)
        test.append(TopLeftLatitude)
        test.append(TopRightLongitude)
        test.append(TopRightLatitude)
        test.append(BottomRightLongitude)
        test.append(BottomRightLatitude)
        test.append(BottomLeftLongitude)
        test.append(BottomLeftLatitude)
        test.append(int(float(root.find('CloudPercent').text)))
        excel_data.append(test)
    return excel_data


def create_polygon(info):
    df = pd.DataFrame(info)
    ## 生成线矢量文件 ##
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource("Polygon.shp")  ## shp文件名称
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  ## 空间参考：WGS84
    layer = data_source.CreateLayer("Polygon", srs, ogr.wkbPolygon)  ## 图层名称要与shp名称一致
    nameList = ['数据名称', '卫星名称', '获取时间', '产品级别', '云量', '侧视角', '投影方式', '地球模型', '空间分辨率',
                '波段组合',
                '左上角X', '左上角Y', '右上角X', '右上角Y', '右下角X', '右下角Y', '左下角X', '左下角Y', '数据类型',
                '处理级别',
                '重采样方式', '数据格式', '景号', '产品号']
    try:
        for namel in nameList:
            field_name = ogr.FieldDefn(namel, ogr.OFTString)  ## 设置属性
            field_name.SetWidth(50)  ## 设置长度
            layer.CreateField(field_name)  ## 创建字段
    except:
        pass

    feature = ogr.Feature(layer.GetLayerDefn())
    for iter in range(1, df.shape[0]):
        shujuName = df.loc[iter][1] + '_' + str(df.loc[iter][2]) + '_L2A0000' + str(df.loc[iter][4]) + '_' + str(
            df.loc[iter][0]) + '_01'
        feature.SetField(nameList[0], shujuName)  ## 设置字段值
        feature.SetField(nameList[1], df.loc[iter, 1])  ## 设置字段值
        feature.SetField(nameList[2], df.loc[iter, 2])  ## 设置字段值
        feature.SetField(nameList[3], 'LEVEL2A')  ## 设置字段值
        feature.SetField(nameList[4], df.loc[iter, 14])  ## 设置字段值
        feature.SetField(nameList[5], df.loc[iter, 5])  ## 设置字段值
        feature.SetField(nameList[6], 'UTM')  ## 设置字段值
        feature.SetField(nameList[7], 'WGS-84')  ## 设置字段值
        feature.SetField(nameList[8], '0.5/2')  ## 设置字段值
        feature.SetField(nameList[9], '1,2,3,4')  ## 设置字段值
        feature.SetField(nameList[10], str(round(float(df.loc[iter, 6]), 2)))  ## 设置字段值
        feature.SetField(nameList[11], str(round(float(df.loc[iter, 7]), 2)))  ## 设置字段值
        feature.SetField(nameList[12], str(round(float(df.loc[iter, 8]), 2)))  ## 设置字段值
        feature.SetField(nameList[13], str(round(float(df.loc[iter, 9]), 2)))  ## 设置字段值
        feature.SetField(nameList[14], str(round(float(df.loc[iter, 10]), 2)))  ## 设置字段值
        feature.SetField(nameList[15], str(round(float(df.loc[iter, 11]), 2)))  ## 设置字段值
        feature.SetField(nameList[16], str(round(float(df.loc[iter, 12]), 2)))  ## 设置字段值
        feature.SetField(nameList[17], str(round(float(df.loc[iter, 13]), 2)))  ## 设置字段值
        feature.SetField(nameList[18], '栅格数据')  ## 设置字段值
        feature.SetField(nameList[19], 'LEVEL2A')  ## 设置字段值
        feature.SetField(nameList[20], 'BL')  ## 设置字段值
        feature.SetField(nameList[21], 'TIFF')  ## 设置字段值
        feature.SetField(nameList[22], df.loc[iter, 3])  ## 设置字段值
        feature.SetField(nameList[23], df.loc[iter, 4])  ## 设置字段值
        wkt = "POLYGON((" + str(df.loc[iter, 6]) + " " + str(df.loc[iter, 7]) + ", " + \
              str(df.loc[iter, 8]) + " " + str(df.loc[iter, 9]) + ", " + \
              str(df.loc[iter, 10]) + " " + str(df.loc[iter, 11]) + ", " + \
              str(df.loc[iter, 12]) + " " + str(df.loc[iter, 13]) + "))"  ## 创建面
        polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
        feature.SetGeometry(polygon)  ## 设置面
        layer.CreateFeature(feature)  ## 添加面，可以添加多个面
    feature = None  ## 关闭属性
    data_source = None  ## 关闭数据
    print('已完成')


a = huoquInfo(r'C:\Users\QYSM\Desktop\安徽xml及落图\SV/')
create_polygon(a)
