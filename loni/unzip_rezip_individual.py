path_src = '/scratch/hanganua/database/loni_adni/source/mri_big'
tmp_unzip = '/scratch/hanganua/database/loni_adni/source/mri_unzipped'
path_dst = '/home/hanganua/projects/def-hanganua/adni/source/mri'
archive_type = '.zip'

from os import listdir, path, system, chdir, getcwd
import shutil


class Extract_Individual():

    def __init__(self, path_src, tmp_unzip, path_dst, depth = '', rename=''):
        self.tmp_unzip = tmp_unzip
        self.path_dst = path_dst
        self.ls_mribig = [i for i in listdir(path_src) if archive_type in i]
        for file in self.ls_mribig:
            print('unzipping: ',file)
            system('unzip -q '+path.join(path_src, file)+' -d '+tmp_unzip)
            if depth:
                 self.tmp_unzip = self.deep(depth)
            print(self.tmp_unzip)
            if rename:
                self.rename(rename)
            self.rezip_individually()
            self.move_to_dst()
            system("mv "+path.join(path_src, file)+" "+path.join(path_src, '2del_'+file))

    def deep(self, deep):
        return path.join(self.tmp_unzip, listdir(self.tmp_unzip)[0])

    def rename(self, rename):
        chdir(self.tmp_unzip)
        ls_dirs = listdir(getcwd())
        for folder in ls_dirs:
            print('renaming: ', folder," to ",rename+folder,len(ls_dirs[ls_dirs.index(folder):])," left")
            system('mv '+folder+' '+rename+folder)

    def rezip_individually(self):
        chdir(self.tmp_unzip)
        ls_dirs = listdir(getcwd())
        for folder in ls_dirs:
            print('archiving: ', folder,"; ",len(ls_dirs[ls_dirs.index(folder):])," left")
            system('zip -r -q -m '+folder+'.zip '+folder)

    def move_to_dst(self):
        for file_zip in listdir(self.tmp_unzip):
            print('moving: '+path.join(self.tmp_unzip, file_zip)+' '+self.path_dst)
            system('mv '+path.join(self.tmp_unzip, file_zip)+' '+self.path_dst)
            system('chmod 777 '+path.join(self.path_dst, file_zip))


Extract_Individual(path_src, tmp_unzip, path_dst, 1, 'ADNI_')


'''
lsbig = [
"adni_download2_14.zip",  adni_download2_19.zip  adni_download2_23.zip  adni_download2_6.zip
"adni_download2_10.zip",  adni_download2_15.zip  adni_download2_1.zip   adni_download2_2.zip   adni_download2_7.zip
"adni_download2_11.zip",  adni_download2_16.zip  adni_download2_20.zip  adni_download2_3.zip   adni_download2_8.zip
"adni_download2_12.zip",  adni_download2_17.zip  adni_download2_21.zip  adni_download2_4.zip   adni_download2_9.zip
"adni_download2_13.zip",  adni_download2_18.zip  adni_download2_22.zip  adni_download2_5.zip   MRI1.5T_IRR_V00.zip]
'''



