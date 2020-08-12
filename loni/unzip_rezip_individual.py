username = 'hanganua'
from os import listdir, path, system, chdir, getcwd

path_src = path.join('/scratch', username, 'database', 'loni_adni', 'source', 'mri_big')
tmp_unzip = path.join('/scratch', username, 'database', 'loni_adni', 'source', 'mri_unzipped')
unzipped = path.join('/scratch', username, 'database', 'loni_adni', 'source', 'mri_unzipped', 'ADNI')
path_dst = path.join('/home', username, 'projects', 'def-'+username, 'adni', 'source', 'mri')
archive_type = '.zip'


class Extract_Individual():

    def __init__(self, path_src, tmp_unzip, unzipped, path_dst, rename=''):
        self.unzipped = unzipped
        self.path_dst = path_dst
        self.ls_mribig = [i for i in listdir(path_src) if archive_type in i]
        for file in self.ls_mribig:
            print('unzipping: ',file)
            system('unzip -q '+path.join(path_src, file)+' -d '+tmp_unzip)
            if rename:
                self.rename(rename)
            self.rezip_individually()
            self.move_to_dst()
            system("mv "+path.join(path_src, file)+" "+path.join("/scratch", "hanganua", "database", "loni_adni", "source", "2del", '2del_'+file))

    def rename(self, rename):
        chdir(self.unzipped)
        ls_dirs = listdir(getcwd())
        for folder in ls_dirs:
            if 'rename' not in folder:
                print('renaming: ', folder," to ", rename+folder, len(ls_dirs[ls_dirs.index(folder):])," left")
                system('mv '+folder+' '+rename+folder)

    def rezip_individually(self):
        chdir(self.unzipped)
        ls_dirs = listdir(getcwd())
        for folder in ls_dirs:
            print('archiving: ', folder,"; ",len(ls_dirs[ls_dirs.index(folder):])," left")
            system('zip -r -q -m '+folder+'.zip '+folder)

    def move_to_dst(self):
        for file_zip in listdir(self.unzipped):
            print('moving: '+path.join(self.unzipped, file_zip)+' '+self.path_dst)
            system('mv '+path.join(self.unzipped, file_zip)+' '+self.path_dst)
            system('chmod 777 '+path.join(self.path_dst, file_zip))


Extract_Individual(path_src, tmp_unzip, unzipped, path_dst, 'ADNI_')



