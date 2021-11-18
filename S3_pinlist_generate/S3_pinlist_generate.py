# S3_pinlist_generate.py
#
# Created on: 11/15/2021
#     Author: Anyka
#      		  Phoebe Luo
import re
import os
import sys
import xlrd
import os.path
from os import path

# ----------------------------------Input Intended Pinlist Information for Generation-----------------------------------
# input path of the Excel file
excel_path = r"/home/luozx/work/S3_pinlist_generate/Snowbird3_pinlist_V1.1.2.xls"
# input path of the pin mux v files
pin_mux_v_path = r"/home/luozx/work/S3_pinlist_generate/pin_mux_new"
# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------Part 1. Functions---------------------------------------------------
# Function 1. turn string to lower case
def tolowercase(string):
    string = string.lower()
    return string


# Function 2. for pinlist, change port number to the correct format for writing file
def fileportnum(num):
    if len(num) == 1:
        # if port number is a one digit int, add 0 to front to fit format
        num = "0" + num
    return num


# Function 3. for pinlist, change port number to the correct format for reading Excel
def excelportnum(num):
    if len(num) == 2 and num[0] == "0":
        # if port number is a one digit int written in two digit, remove 0 at front to fit format
        num = num[1]
    # if port number is 0, change to format GPIO0_Boot(I/O)
    if num == "0":
        num = "0_Boot"
    return num


# --------------------------------------------Part 2. Function to read list---------------------------------------------
def getpinmuxlist(num):
    # list_total to hold all the function names extracted from Excel
    list_total = []

    # 1. get row amd column number of designated port
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name("pin_list")
    excel_num = excelportnum(num)
    row_loc = -1
    col_loc = -1
    # identify that the functions will be a different format in the Excel or the normal format under Func0
    func_form = 0
    # to make sure that the port row and col is only updated once
    check_port = 0

    for col in range(table.ncols):
        for row in range(table.nrows):
            # find the col of the Func0 to locate the port
            if table.cell_value(row, col) == "Func0" or table.cell_value(row, col) == "Func0\n":
                func0_col = col

            # find the port cell row and col
            if (table.cell_value(row, col) == "GPIO" + excel_num + "(I/O)" or table.cell_value(row, col) == " GPIO" + excel_num + "(I/O)") and col == func0_col and check_port == 0:
                # locate the row and column number of GPIO(I/O)
                row_loc = row
                col_loc = col
                # identify that the port has already been looked at
                check_port = 1
            elif (table.cell_value(row, col) == "GPIO" + excel_num + "(I/O)" or table.cell_value(row, col) == " GPIO" + excel_num + "(I/O)") and col != func0_col and check_port == 0:
                # locate the row and column number of GPIO(I/O)
                row_loc = row
                col_loc = col
                # identify that the functions will be a different format
                func_form = 1
                # identify that the port has already been looked at
                check_port = 1

    if row_loc == -1 and col_loc == -1:
        # the GPIO port is not under column Func0
        print("Error: chart format not correct, GPIO" + excel_num + " is not found in the Excel file")
        return 0

    # 2, write the GPIO port info into file
    if func_form == 1:
        writepinmuxfile(excel_num, num, 0, 1)
    else:
        writepinmuxfile(excel_num, num, 0)

    # 3. update list with all the function names
    if func_form == 0:
        list_total[:] = table.row_values(row_loc, col_loc + 1, col_loc + 6)
        while list_total.count("") != 0:
            list_total.remove("")
        if len(list_total) == 0:
            # the GPIO port has no function
            print("Error: chart format not correct, GPIO" + excel_num + " has no function")
            return 0
    elif func_form == 1:
        list_total = []
        list_total.append(table.cell_value(row_loc, col_loc - 1))

    # 4. go through the list to identify I/O, change name format, and call to write to file
    for element in list_total:
        if element.find("(i/o)") >= 0 or element.find("(I/O)") >= 0:
            # strip the (I/O) part
            element = element[:len(element) - 5]
            # write to file
            writepinmuxfile(element, num, 1)
        elif element
