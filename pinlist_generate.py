# pinlist_generate.py
#
# Created on: 09/28/2021
#     Author: Anyka
#      		  Phoebe Luo

import xlrd
import re

# -----------------------------------Input Intended Pinlist Information for Generation----------------------------------
# input path of the excel file
excel_path = r"/home/luozx/work/pinlist_generate/SnowbirdT5_MWP2_Pinlist_V0.0.5.xls"
# input path of the pinlist sv files
seq_sv_path = r"/home/luozx/work/pinlist_generate/seq"
# input path of the pinlist test sv files
test_sv_path = r"/home/luozx/work/pinnlist_generate/test"
#input path of the interface sv file
sv_path = r"/home/luozx/work/interface_generate"
# ----------------------------------------------------------------------------------------------------------------------

# Function 1.turn string to lower case
def tolowercase(string):
    string = string.lower()
    return string

# Function 2. fo pinlist, concat the function name with _input and _output
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
def getbitwidth(string, num):
    if string.find("[") >= 0 and string.find("]") >= 0:
        # get the bit width number
        find_width = string[string.find("["):string.find("]")]
        width = re.findall(r'\d+', find_width)[0]
        # strip the width
        string = string[:string.find("[")]

        # if it is marked as input, format as _in concat width
        if num == 0:
            # check if the ending already has _in
            string = checkending(string, 0)
            string = string + "_in" + width
            width_list.append(string)
        # if it is marked as output, format as _out concat width
        elif num == 1:
            # check if the ending already has _out
            string = checkending(string, 1)
            string = string + "_out" + width
            width_list.append(string)

    return string


# Function 7. for pinlist, check the last section of the module name to return the formatted name
def checklastsec(string, num):
    if string.find("_") >= 0:
        list_sec = string.split("_")
        # extract the width number from the last section
        width_num = re.findall(r'\d+', list_sec[-1])[0]
        # extract the function name without the width number
        width_func = "_".join(list_sec[:-1]) + "_" + "".join(i for i in list_sec[-1] if not i.isdigit())
        if num == 0:
            # if it is marked as input
            string = width_func + "[" + width_num + "]"
        elif num == 1:
            # if it is marked as output
            string = width_func + "(" + width_num
    return string


# Function 8. for pinlist, check the last section of the module name to return the formatted name without the width
def striplastsec(string):
    if string.find("_") >= 0:
        list_sec = string.split("_")
        # extract the function name without the width number
        width_func = "_".join(list_sec[:-1]) + "_" + "".join(i for i in list_sec[-1] if not i.isdigit())
    return width_func

# FUnction 9. for both pinlist and interface, check the last section o fthe name and if _in and _out appears, strip the _in or _out
def checkending(string, num):
    # check if the name already has _in as an ending
    if num == 0:
        if string.find("_in") == len(string) - 3:
            string = string[:len(string) - 3]
    # check if the name already has _out as an ending
    elif num == 1:
        if string.find("_out") == len(string) - 4:
            string = string[:len(string) - 4]
    return string


# ----------------------------------Part 1. Function to extract Excel info for pinlist----------------------------------
def getlist(num):
def getlist(num):
    # list_total to hold all the function names extracted from Excel
    list_total = []
    # list1 to hold all the function names that are formatted
    list1 = []

    # 1. get row and column number of designated port
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name("pin_list")
    num = excelportnum(num)

    for col in range(table.ncols):
        for row in range(table.nrows):
            if table.cell_value(row, col) == "Func0" or table.cell_value(row, col) == "Func0\n":
                func0_col = col
            if table.cell_value(row, col) == "GPIO" + num + "(I/O)" and col == func0_col:
                # locate the row and column number of GPIO(I/O)
                row_loc = row
                col_loc = col
            elif table.cell_value(row, col) == "GPIO" + num + "(I/O)" and col != func0_col:
                # the GPIO port is not under column Func0
                print("Error: chart format not correct, GPIO" + num + " is not found under Func0")
                return 0

    # 2. update list with all the function names
    list_total[:] = table.row_values(row_loc, col_loc + 1, col_loc + 12)
    while list_total.count("") != 0:
        list_total.remove("")

    # 3. go through the list to identify I/O, change name format, and put into list1
    for element in list_total:
        if element.find("(i)") >= 0 or element.find("(I)") >= 0:
            # the names that go into list1
            element = element[:len(element) - 3]
            # change name format
            element = tolowercase(element)
            element = getbitwidth(element, 0)
            func_element = listconcat(element, 0)
            # add name to function name
            list1.append(func_element)
        elif element.find("(o)") >= 0 or element.find("(O)") >= 0:
            # the names that go into list1
            element = element[:len(element) - 3]
            # change name format
            element = tolowercase(element)
            element = getbitwidth(element, 1)
            func_element = listconcat(element, 1)
            # add name to function name
            list1.append(func_element)
        elif element.find("(i/o)") >= 0 or element.find("(I/O)") >= 0:
            # the names that go into list1
            element = element[:len(element) - 5]
            # change name format
            element = tolowercase(element)
            func_in_element = getbitwidth(element, 0)
            func_out_element = getbitwidth(element, 1)
            func_in_element = listconcat(func_in_element, 0)
            func_out_element = listconcat(func_out_element, 1)
            # add name to function name
            list1.append(func_in_element)
            list1.append(func_out_element)
        else:
            print("Error: chart format not correct, I/O information not found for " + element)
    return list1
    

# ---------------------------------------Part 2. Function to write to seq sv file---------------------------------------
def writeseqfile(list1, num):


# ---------------------------------------Part 3. Function to write to test sv file--------------------------------------
def writetestfile(num):


# ---------------------------------Part 4. Function to extract Excel info for interface---------------------------------
def getinterfacelist(num):


# ------------------------------------Part 5. Function to write to interface sv file------------------------------------
def writesvfile():


# --------------------------------------Part 6. Global strings to write to sv file--------------------------------------
string_1 = ""
string_2 = ""


# -----------------------------------------------------Part 7. Main-----------------------------------------------------
# function names for interface
func_norm_list = []
# function with bit width for interface
func_width_list = []

for i in range(1, 41):
    num = str(i)
    getinterfacelist(num)
    port_num = fileportnum(num)
    # input path of the seq sv file
    seq_path = seq_sv_path + "/gpio_" + port_num + "_new_domain_seq.sv"
    # input path of the test sv file
    test_path = test_sv_path + "/gpio_" + port_num + "_new_domain_test.sv"
    # function names
    func_list = []
    # function with width
    width_list = []

    func_list = getlist(port_num)
    if func_list == 0:
        continue
    writeseqfile(func_list, port_num)
    writetestfile(port_num)

sv_path = sv_path + "/pin_mux_interface_new.sv"
writesvfile()
