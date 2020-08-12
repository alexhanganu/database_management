"""
processed data is stored as zip archived
these scripts allow extraction of specific folders
stats - for extraction of statistics
label and surf = for glm analysis with mris_glmfit

"""

from os import path, makedirs, listdir

PROCESSED_FS = path.join("/home", "lucaspsy", "database", "loni_adni", "processed_fs")
path_2_extract = path.join("/scratch", "lucaspsy", "subjects_glm")

folders2_extract = ["label","surf"]


# ---------------------------------

import zipfile

def read_zip(path2file, file):
        return zipfile.ZipFile(path.join(path2file,file), 'r')


def zip_file_content(zip_f):
        return zip_f.namelist()


def xtrct_dirs(zip_f, _ls_content, path_2_extract, pattern=""):
    for val in _ls_content:
        if pattern in val:
            try:
                zip_f.extract(val, path=path_2_extract)
            except Exception as e:     
                print(e)                                                                     
                pass                                                                 


if __name__ == "__main__":
    if not path.exists(path_2_extract):
        makedirs(path_2_extract)


    for zip in listdir(PROCESSED_FS):
        print("extracting: "+ zip)
        zip_file = read_zip(PROCESSED_FS, zip)
        if '_v2' in zip:
            subjid = zip.strip(".zip")
        else:
            subjid = zip.strip(".zip")[:-11]
        for folder in [path.join(subjid, i) for i in folders2_extract]:
            print("    for pattern: ",folder)
            xtrct_dirs(zip_file, 
                       zip_file_content(zip_file),
                       path_2_extract, 
                       pattern = folder)

