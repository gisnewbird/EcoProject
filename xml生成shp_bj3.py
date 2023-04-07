import glob
import os
from xml.etree import ElementTree as ET

import pandas as pd
from osgeo import ogr, osr, gdal


def huoquInfo(path_base):
    if (os.path.exists(path_base)):
        f = glob.glob(path_base + '/*.xml')
    df = pd.DataFrame()
    excel_data = [['数据名称', '卫星', '成像开始时间', '景号', '产品号', '视角',
                   '左上角经度', '左上角纬度', '右上角经度', '右上角纬度', '右下角经度', '右下角纬度', '左下角经度',
                   '左下角纬度',
                   '云量']]
    c = 1  # 行
    for file in f:
        # print (file)
        test = []
        # 打开文件
        dom = ET.parse(file)
        # 文档根元素
        root = dom.getroot()
        # 四角点坐标
        TopLeftLongitude = round(float(root.find('Image_Extent').findall('Vertex')[0].find('LON').text), 5)
        TopLeftLatitude = round(float(root.find('Image_Extent').findall('Vertex')[0].find('LAT').text), 5)
        TopRightLongitude = round(float(root.find('Image_Extent').findall('Vertex')[1].find('LON').text), 5)
        TopRightLatitude = round(float(root.find('Image_Extent').findall('Vertex')[1].find('LAT').text), 5)
        BottomRightLongitude = round(float(root.find('Image_Extent').findall('Vertex')[2].find('LON').text), 5)
        BottomRightLatitude = round(float(root.find('Image_Extent').findall('Vertex')[2].find('LAT').text), 5)
        BottomLeftLongitude = round(float(root.find('Image_Extent').findall('Vertex')[3].find('LON').text), 5)
        BottomLeftLatitude = round(float(root.find('Image_Extent').findall('Vertex')[3].find('LAT').text), 5)
        test.append(root.find('Product_Identification').find('DATASET_NAME').text)
        test.append(root.find('General_Information').find('IMAGING_SATELLITE').text)
        test.append(root.find('Product_Information').find('IMAGING_TIME_UTC').text.split('T')[0].replace('-', ''))
        test.append(' ')
        test.append(' ')
        test.append(int(float(root.find('Geometric_Data').find('Use_Area').findall('Located_Geometric_Values')[2].
                              find('Acquisition_Angles').find('VIEW_ANGLE').text)))
        test.append(TopLeftLongitude)
        test.append(TopLeftLatitude)
        test.append(TopRightLongitude)
        test.append(TopRightLatitude)
        test.append(BottomRightLongitude)
        test.append(BottomRightLatitude)
        test.append(BottomLeftLongitude)
        test.append(BottomLeftLatitude)
        test.append(int(float(root.find('Quality_Assessment').find('Cloud_Cover').find('CLOUD_COVER_RATIO').text)))
        excel_data.append(test)
    return excel_data


def create_polygon(info):
    df = pd.DataFrame(info)
    ## 生成线矢量文件 ##
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    strVectorFile = "test1.shp"  # 定义写入路径及文件名
    ogr.RegisterAll()  # 注册所有的驱动
    strDriverName = "ESRI Shapefile"  # 创建数据，这里创建ESRI的shp文件
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)

    oDS = oDriver.CreateDataSource(strVectorFile)  # 创建数据源
    if oDS == None:
        print("创建文件【%s】失败！", strVectorFile)

    srs = osr.SpatialReference()  # 创建空间参考
    srs.ImportFromEPSG(4326)  # 定义地理坐标系WGS1984
    papszLCO = []
    # 创建图层，创建一个多边形图层,"TestPolygon"->属性表名
    oLayer = oDS.CreateLayer("TestPolygon", srs, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")

    # layer = data_source.CreateLayer("Polygon", srs, ogr.wkbPolygon)  ## 图层名称要与shp名称一致
    name_list = ['数据名称', '卫星名称', '获取时间', '产品级别', '云量', '侧视角', '投影方式', '地球模型', '空间分辨率',
                 '波段组合', '左上角X', '左上角Y', '右上角X', '右上角Y', '右下角X', '右下角Y', '左下角X', '左下角Y',
                 '数据类型', '处理级别', '重采样方式', '数据格式', '景号', '产品号']
    try:
        for namel in name_list:
            field_name = ogr.FieldDefn(namel, ogr.OFTString)  ## 设置属性
            field_name.SetWidth(50)  ## 设置长度
            oLayer.CreateField(field_name)  ## 创建字段
    except:
        pass

    feature = ogr.Feature(oLayer.GetLayerDefn())
    for iter in range(1, df.shape[0]):
        shujuName = df.loc[iter][0]
        feature.SetField(name_list[0], shujuName)  ## 设置字段值
        feature.SetField(name_list[1], df.loc[iter, 1])  ## 设置字段值
        feature.SetField(name_list[2], df.loc[iter, 2])  ## 设置字段值
        feature.SetField(name_list[3], 'LEVEL2A')  ## 设置字段值
        feature.SetField(name_list[4], df.loc[iter, 14])  ## 设置字段值
        feature.SetField(name_list[5], df.loc[iter, 5])  ## 设置字段值
        feature.SetField(name_list[6], 'UTM')  ## 设置字段值
        feature.SetField(name_list[7], 'WGS-84')  ## 设置字段值
        feature.SetField(name_list[8], '0.5/2')  ## 设置字段值
        feature.SetField(name_list[9], '1,2,3,4')  ## 设置字段值
        feature.SetField(name_list[10], str(round(df.loc[iter, 6], 2)))  ## 设置字段值
        feature.SetField(name_list[11], str(round(df.loc[iter, 7], 2)))  ## 设置字段值
        feature.SetField(name_list[12], str(round(df.loc[iter, 8], 2)))  ## 设置字段值
        feature.SetField(name_list[13], str(round(df.loc[iter, 9], 2)))  ## 设置字段值
        feature.SetField(name_list[14], str(round(df.loc[iter, 10], 2)))  ## 设置字段值
        feature.SetField(name_list[15], str(round(df.loc[iter, 11], 2)))  ## 设置字段值
        feature.SetField(name_list[16], str(round(df.loc[iter, 12], 2)))  ## 设置字段值
        feature.SetField(name_list[17], str(round(df.loc[iter, 13], 2)))  ## 设置字段值
        feature.SetField(name_list[18], '栅格数据')  ## 设置字段值
        feature.SetField(name_list[19], 'LEVEL2A')  ## 设置字段值
        feature.SetField(name_list[20], 'CC')  ## 设置字段值
        feature.SetField(name_list[21], 'TIFF')  ## 设置字段值
        feature.SetField(name_list[22], df.loc[iter, 3])  ## 设置字段值
        feature.SetField(name_list[23], df.loc[iter, 4])  ## 设置字段值
        wkt = "POLYGON((" + str(df.loc[iter, 6]) + " " + str(df.loc[iter, 7]) + ", " + \
              str(df.loc[iter, 8]) + " " + str(df.loc[iter, 9]) + ", " + \
              str(df.loc[iter, 10]) + " " + str(df.loc[iter, 11]) + ", " + \
              str(df.loc[iter, 12]) + " " + str(df.loc[iter, 13]) + "))"  ## 创建面
        polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
        feature.SetGeometry(polygon)  ## 设置面
        oLayer.CreateFeature(feature)  ## 添加面，可以添加多个面
    # feature = None  ## 关闭属性
    # data_source = None  ## 关闭数据
    print('已完成')


a = huoquInfo(r'C:\Users\QYSM\Desktop\BJ3A/')
create_polygon(a)
