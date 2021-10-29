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


# Function 3. for pinlist, change port number to the correct format for writing file
def fileportnum(num):
    if len(num) == 1:
        # if port number is a one digit int, add 0 to front to fit bit format
        num = "0" + num
    return num


# Function 4. for pinlist, change port number to the port number to the correct format for reading Excel
def excelportnum(num):
    if len(num) == 2 and num[0] == "0":
        # if port number is a one digit int written in two digit, remove 0 at front to fit format
        num = num[1]
        return num


# Function 5. for interface, look for bit width and reformat function name, update the corresponding list
def reformname(string, num):
    # if the function name is with width
    if string.find("[") >= 0 and string.find("]") >= 0:
        # if it has width, delete the width
        string = string[:string.find("[")]
        # if it is marked as input, format as _in and add it into func_Width_list
        if num == 0:
            # check if the name already has _in
            string = checkending(string, 0)
            string = string + "_in"
        # if it is marked as output, format as _out and add it into func_width_list
        elif num == 1:
            # check if the name already has _out
            string = checkending(string, 1)
            string = string + "_out"

        # if the name is already in func_width_list do not add into the list
        if not(string in func_width_list):
            func_width_list.append(string)

    # if the function name is not with width
    else:
        # if it is marked as input, format as _in and add it into func_norm_list
        if num == 0:
            # check if the ending already has _in
            string = checkending(string, 0)
            string = string + "_in"
        # if it is marked as output, format as _out and add it into func_norm_list
        elif num == 1:
            # check if the ending already has _out
            string = checkending(string, 1)
            string = string + "_out"

        # if the name is already in func_norm_list do not add into the list
        if not (string in func_norm_list):
            func_norm_list.append(string)


# Function 6. for pinlist, look for bit width and reformat it
