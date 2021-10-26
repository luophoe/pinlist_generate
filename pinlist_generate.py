# pinlist_generate.py
#
# Created on: 09/28/2021
#     Author: Anyka
#      		  Phoebe Luo

import xlrd
import re

# --------------------------------Input Intended Pinlist Information for Generation--------------------------------
# input path of the excel file
excel_path = r"/home/luozx/work/pinlist_generate/SnowbirdT5_MWP2_Pinlist_V0.0.5.xls"
# input path of the pinlist sv files
seq_sv_path = r"/home/luozx/work/pinlist_generate/seq"
# input path of the pinlist test sv files
test_sv_path = r"/home/luozx/work/pinnlist_generate/test"
#input path of the interface sv file
sv_path = r"/home/luozx/work/interface_generate"
# ------------------------------------------------------------------------------------------------------------------

# Function 1.turn string to lower case
def tolowercase(string):
    string = string.lower()
    return string

# Function 2. concat the function name with _input and _output
def listconcat(string, num):
    if num == 0:
        # concat _input
        string = string + "_input"
    elif num == 1:
        # concat _output
        string = string + "_output"
    return string

