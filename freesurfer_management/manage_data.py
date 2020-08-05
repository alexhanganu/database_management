"""
processed data is stored as zip archived
yhese scripts allow extraction of specific folders in orser to do the 
stats extraction or glm analysis

specifically for LONI databases, a function is written that 
extracts the dates of MRI acquisitions that were used for 
FreeSurfer processing
"""

from os import path, makedirs, listdir
import zipfile

PROCESSED_FS = path.join("/scratch", "hanganua", "database", "loni_adni", "processed_fs")
path_2_extract = path.join("/scratch", "hanganua", "reconlog")#"stats")



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

    folders2_extract = ["scripts/recon-all.log",] #["stats",]# "label","surf"]

    for zip in listdir(PROCESSED_FS):
        print("extracting: "+ zip)
        zip_file = read_zip(PROCESSED_FS, zip)
        for folder in [path.join(zip.strip(".zip"), i) for i in folders2_extract]:
            xtrct_dirs(zip_file, 
                       zip_file_content(zip_file),
                       path_2_extract, 
                       pattern = folder)

