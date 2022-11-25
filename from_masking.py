#user : rajatbansal

import pandas as pd
import os
import shutil
def find_file(DOCUEMNT_NAME	, folder_to_search):
    ops = 0
    for root, dirs, files in os.walk(folder_to_search):
        ops += 1
        if DOCUEMNT_NAME	 in files:
            print(os.path.join(root, DOCUEMNT_NAME	))
            return os.path.join(root, DOCUEMNT_NAME	)
    # print("ops: ", ops)
    return "No"

def copy_files(excel_file, folder_to_search, target_folder):
    count = 0
    data = pd.read_excel(excel_file, sheet_name="final")
    try:
        os.mkdir(target_folder)
    except FileExistsError:
        print("Folder already exists")

    for file in data.DOCUEMNT_NAME.values:
        result = find_file(file, folder_to_search)
        try:
            if result != "No":
                shutil.copy(result, os.path.join(target_folder, file))
                count += 1
        except Exception as e:
            print(e)
    print("Total files: ", len(data.DOCUEMNT_NAME))
    print("Files copied: ", count)
    print("Files not found: ", len(data.DOCUEMNT_NAME) - count)

if __name__ == "__main__":
    excel_file = "AADHAR_STATUS_03102022_Manmaya.xls"
    # folder_to_search = r"/Data/StarHealth/uploads/masking/"
    # target_folder = r"/Data/StarHealth/from_masking/"
    folder_to_search = "files"
    target_folder = "sorted"
    copy_files(excel_file, folder_to_search, target_folder)