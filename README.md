# pinlist_generate
- a Python script to autogenerate SystemVerilog test files for RTL verification. The main function is to read pin list from an Excel file(.xls), extract the function names of the GPIO ports, reformat the names to generate vaild SystemVerilog codes, and output as seq, test, and interface files for RTL verification (provided file is simplified version and the original file is confidential)
- due to different standards of writing to the Excel file between departments, the script must turn different writing style into the same format in order to get consistent output
- output gpio_xx_domain_seq.sv and gpio_xx_domain_test SystemVerilog files for all the ports documented in the Excel file and output pin_mux_interface.sv SystemVerilog file for the entire pinlist
- have 2 version for project T5 (short for SnowbirdT5) and S3 (short for Snowbird3)
