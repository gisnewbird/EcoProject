# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import ttk

import shapefile
from osgeo import osr
from ttkthemes.themed_tk import ThemedTk

# Create the main window
root = ThemedTk(theme="white")
root.title("计算固土价值")
root.geometry("500x110+{}+{}".format(root.winfo_screenwidth() // 2 - 400, root.winfo_screenheight() // 2 - 300))
# Create the text box with a border and smaller size
label = Label(root, text='请输入矢量文件的绝对路径:', font=("Helvetica", 16))
label.pack()
text_box = ttk.Entry(root, width=40, font=("Helvetica", 16), style="Custom.TEntry")
text_box.pack()

# Create a custom style for the buttons
style = ttk.Style()
style.configure("Custom.TButton", background="white", foreground="black", font=("Helvetica", 16))


# 林地土壤侵蚀模数
# 阔叶林：0.4922；油松林：0.8645；侧柏林：0.6334；
# 落叶松林：0.2482；油松侧柏混交林：0.7490；油松阔叶混交林：0.6612；
# 侧柏阔叶混交林：0.5457；油松侧柏阔叶混交林：0.6519；灌木林：0.8000
def lindiqinshimoshu(shuzhong):
    if shuzhong == '阔叶林':
        return 0.4947
    if shuzhong == '油松林':
        return 0.8645
    if shuzhong == '侧柏林':
        return 0.6334
    if shuzhong == '落叶松林':
        return 0.2482
    if shuzhong == '油松侧柏混交林':
        return 0.7490
    if shuzhong == '油松阔叶混交林':
        return 0.6796
    if shuzhong == '侧柏阔叶混交林':
        return 0.5641
    if shuzhong == '油松侧柏阔叶混交林':
        return 0.6642
    if shuzhong == '灌木林':
        return 0.8000
    else:
        return 0.0


def wulindimoshu(year):
    if year == '2018':
        return 5.97
    if year == '2019':
        return 4.44
    if year == '2020':
        return 5.76
    if year == '2021':
        return 4.2661
    else:
        return 0.0


# 价值量等于固土量*挖取单位面积土方费用(33.8136 /t.a)
def algorithm(input_text):
    try:
        # Read the shapefile
        sf = shapefile.Reader(input_text.replace('\\', '/'), encoding="gbk")
        outpath = input_text.replace('\\', '/').replace('.shp', '_out.shp')
        w = shapefile.Writer(outpath, shapeType=sf.shapeType, encoding="gbk")
        w.fields = list(sf.fields)
        # 新增加两个字段
        w.field("固土价值", "F", 8)
        # Get the field names and index of the desired attribute
        fields = sf.fields[1:]
        field_names = [field[0] for field in fields]
        year_index = field_names.index('年份')
        area_index = field_names.index('面积')
        tree_index = field_names.index('树种')
        # 将另外一个文件中的坐标点的信息存入新增加的两个字段
        i = 0
        for feature in sf.shapeRecords():
            ls = feature.record
            area = feature.record[area_index]
            X1 = float(lindiqinshimoshu(feature.record[tree_index]))
            X2 = float(wulindimoshu(feature.record[year_index]))
            G_gutu = area * (X2 - X1)
            U_gutu = 10.50 * G_gutu
            ls.extend([U_gutu])
            w.record(*ls)
            w.shape(feature.shape)
            i += 1
        w.close()
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        # 或 proj.ImportFromProj4(proj4str)等其他的来源
        wkt = proj.ExportToWkt()
        # 写出prj文件
        f = open(outpath.replace(".shp", ".prj"), 'w')
        f.write(wkt)
        f.close()
        msgbox.showinfo("结果：", "计算完成！")
    except:
        msgbox.showinfo("*错误*", "请检查数据源！")


# Create a frame to hold the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Create the first button
button1 = ttk.Button(button_frame, text="计算固土价值", command=lambda: algorithm(text_box.get()),
                     style="Custom.TButton")
button1.pack()

# Start the main event loop
root.mainloop()
