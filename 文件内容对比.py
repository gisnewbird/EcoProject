# -*- coding:utf-8 -*-
import difflib
import sys


def readfile(filename):
    try:
        fileHandle = open(filename, 'r+')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as error:
        print('Read file Error:' + str(error))
        sys.exit()


def savediffile():
    text1_lines = readfile(textfile1)
    text2_lines = readfile(textfile2)
    d = difflib.HtmlDiff()
    with open('difffile_rpb.html', 'w') as f:
        f.write(d.make_file(text1_lines, text2_lines))


if __name__ == '__main__':
    try:
        textfile1 = r'C:\Users\QYSM\Desktop\GF1,2\1\GF1-PMS\GF1_PMS2_E80.4_N38.0_20230203_L1A0007089999\GF1_PMS2_E80.4_N38.0_20230203_L1A0007089999-MSS2.rpb'
        textfile2 = r'C:\Users\QYSM\Desktop\GF1,2\1\GF1-PMS\12851806001\GF1_PMS2_E35.6_N32.1_20230214_L1A2147483647\GF1_PMS2_E35.6_N32.1_20230214_L1A2147483647-MSS2.rpb'
        savediffile()

    except Exception as e:
        print("Error:" + str(e))
        print("Usage: 3.py filename1 filename2")
        sys.exit()
