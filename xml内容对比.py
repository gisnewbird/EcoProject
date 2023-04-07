from xml.etree import ElementTree as ET

oriPath = r'C:\Users\QYSM\Desktop\GF1,2\1\GF1-PMS\GF1_PMS2_E80.4_N38.0_20230203_L1A0007089999\GF1_PMS2_E80.4_N38.0_20230203_L1A0007089999-MSS2.xml'
comPath = r'C:\Users\QYSM\Desktop\GF1,2\1\GF1-PMS\12851806001\GF1_PMS2_E35.6_N32.1_20230214_L1A2147483647\GF1_PMS2_E35.6_N32.1_20230214_L1A2147483647-MSS2.xml'
# 打开文件
dom_ori = ET.parse(oriPath)
# 文档根元素
root_ori = dom_ori.getroot()
listNames_ori = []
for c in root_ori:  # 通过遍历来获取所有节点
    listNames_ori.append(c.tag)
# 打开文件
dom_cpa = ET.parse(comPath)
# 文档根元素
root_cpa = dom_cpa.getroot()
listNames_cpa = []
for c in root_cpa:  # 通过遍历来获取所有节点
    listNames_cpa.append(c.tag)
print(listNames_ori)
print(listNames_cpa)
print(listNames_ori == listNames_cpa)
