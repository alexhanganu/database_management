path_src = '/scratch/hanganua/database/loni_adni/source/mri_big'
tmp_unzip = '/scratch/hanganua/database/loni_adni/mri_unzipped'
path_dst = '/home/hanganua/projects/def-hanganua/adni/source/mri'
archive_type = '.zip'

from os import listdir, path, system, chdir, getcwd
import shutil


class Extract_Individual():

    def __init__(self, path_src, tmp_unzip, path_dst, deep = '', rename=''):
        self.tmp_unzip = tmp_unzip
        self.path_dst = path_dst
        self.ls_mribig = [i for i in listdir(path_src) if archive_type in i]
        for file in self.ls_mribig[:1]: # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!del
            print('unzipping: ',file)
            system('unzip -q '+path.join(path_src, file)+' -d '+tmp_unzip)
             if deep:
                 self.tmp_unzip = self.deep(deep)
             print(self.tmp_unzip)
#            if rename:
#                self.rename(rename, deep)
#            self.rezip_individually()
#            self.move_to_dst()

    def deeep(self, deep):
        return path.join(self.tmp_unzip, listdir(self.tmp_unzip)[0])


    def rename(self, rename, deep):
        chdir(self.tmp_unzip)
        for file in listdir(getcwd()):
            system('mv '+file+' '+rename+file)

    def rezip_individually(self):
        chdir(self.tmp_unzip)
        ls_dirs = listdir(getcwd())
        for folder in ls_dirs:
            print('archiving: ', folder,"; ",len(ls_dirs[ls_dirs.index(folder):])," left")
            system('zip -r -q -m '+folder+'.zip'+' '+folder)

    def move_to_dst(self):
        for file in self.tmp_unzip:
            print('moving to destination: ',file)
            system('mv '+path.join(self.tmp_unzip, file)+' '+self.path_dst)
            system('chmod 777 '+path.join(self.path_dst, folder+'.zip'))


Extract_Individual(path_src, tmp_unzip, path_dst, deep = 1, 'ADNI_')


'''
lsbig = [
"adni_download2_14.zip",  adni_download2_19.zip  adni_download2_23.zip  adni_download2_6.zip
"adni_download2_10.zip",  adni_download2_15.zip  adni_download2_1.zip   adni_download2_2.zip   adni_download2_7.zip
"adni_download2_11.zip",  adni_download2_16.zip  adni_download2_20.zip  adni_download2_3.zip   adni_download2_8.zip
"adni_download2_12.zip",  adni_download2_17.zip  adni_download2_21.zip  adni_download2_4.zip   adni_download2_9.zip
"adni_download2_13.zip",  adni_download2_18.zip  adni_download2_22.zip  adni_download2_5.zip   MRI1.5T_IRR_V00.zip]
'''



