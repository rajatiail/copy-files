import pandas as pd
import os
import shutil
import time

def find_file(file_name, folder_to_search):
    ops = 0
    for root, dirs, files in os.walk(folder_to_search):
        ops += 1
        if file_name in files:
            print(os.path.join(root, file_name))
            return os.path.join(root, file_name)
    # print("ops: ", ops)
    return "No"

def updatedBYXL(xl_file, folder_to_serach, target_folder, only_no = False , month_year = False, sheet_name = "Sheet1"):
    data = pd.read_excel(xl_file, sheet_name=sheet_name)
    if not month_year:
        print("executing month_year")
        data['AADHAR_REQUEST_DATE'] = pd.to_datetime(data['AADHAR_REQUEST_DATE'])
        data['month_year'] = data['AADHAR_REQUEST_DATE'].dt.strftime('%b_%y').str.upper()
    data['file_name'] = data['DOCUMENT_PATH'].str.split('/').str[-1]
    if only_no:
        print("executing only_no")
        data = data[data.found == "No"]
    data = data.sort_values(by=['month_year'])
    files_count = 0
    transfer = 0
    months = data.month_year.unique()
    for month in months:
        try:
            os.mkdir(os.path.join(target_folder, month))
        except FileExistsError:
            pass
        for file in data[data.month_year == month].file_name:
            files_count += 1
            result = find_file(file, os.path.join(folder_to_serach, month))
            data.loc[data.file_name == file, 'found'] = result
            try:
                if result != "No":
                    shutil.copy(result, os.path.join(target_folder, month, file))
                    transfer += 1
            except exception as e:
                print(e)
    print("Total files with no: ", files_count)
    print("Files Transfered: ", transfer)
    data.to_excel("output_new.xlsx")
    print("excel file saved ....")
    
def sep22(folder_to_search, target_folder, xl_file, sheet_name = "Sheet1"):
    data = pd.read_excel(xl_file, sheet_name=sheet_name)
    data['file_name'] = data['DOCUMENT_PATH'].str.split('/').str[-1]
    months = data.month_year.unique()
    foldersExcludedMonth = set(os.listdir(folder_to_search)) - set(months)

    c = 0
    transfer = 0
    for file in data[(data.found == "No") & (data.month_year == "SEP_22")].file_name.values:
        c += 1
        for folder in foldersExcludedMonth:
            result = find_file(file, os.path.join(folder_to_search , folder))
            data.loc[data.file_name == file, 'found'] = result
            try:
                if result != "No":
                    transfer += 1
                    shutil.copy(result, os.path.join(target_folder, "SEP_22", file))
            except Exception as e:
                print(e)
    data.to_excel("updated_outpt.xlsx")
    print("Total files with no: ", c)
    print("Files Transfered: ", transfer)
    
if __name__ == "__main__":
    xl_file = "input.xlsx"
    folder_to_search = r"/Data/StarHealth/uploads/masking_out/"
    target_folder = r"/Data/StarHealth/14112022/"
    # folder_to_search = "files"
    # target_folder = "sorted"
    now = time.time()
    # updatedBYXL(xl_file, folder_to_search, target_folder)
    sep22(folder_to_search, target_folder, xl_file)
    time_taken = time.time() - now
    print("Time taken: ", time_taken)