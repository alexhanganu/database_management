'''
2020-06-06

script aims to copy from graham to cedar
the folders that were registered and need to undergo further analysis
requires paramiko. On the cluster - this cannot be installed, thus do:
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

choose yes to accept PYTHONPATH change, after the installation:
source ~/.bashrc

conda install paramiko
after that you can use the python from the miniconda, that has paramiko installed

runs with:
cd ~/$USER
./miniconda3/bin/python3.7 scripts/tmp_scp_gra_to_ced.py
'''

username = 'hanganua'
HOST = 'cedar.computecanada.ca'


path_projects = '/home/'+username+'/projects/def-hanganua'
path_src = path_projects+'/fs-subjects' # path that contains the files or folders t$
path_log = path_projects+'/scripts/scp_log.txt' # path where a log file will be stored tha$
path_dst = path_projects #+'/fs-subjects' # path to the remote folder that the files/ folders w$
path_credentials = '/home/'+username # path to the txt-like file named "credentials" that will contain the follow$
dir_name = 'fs_registered'

'''
username = 'string' # username to access the remote computer
mot_de_pass = 'string' # password to access the remote computer
HOST = 'name.address.com' # host name of the remote computer
'''





import os, paramiko, shutil
shutil.copy(path_credentials+'/credentials', os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
try:
        from credentials import mot_de_pass
        os.remove(os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
except ImportError:
        print('file with credentials was not found')
        raise SystemExit()


os.chdir(path_projects)
os.mkdir(path_projects+'/'+dir_name)

for val in [i for i in os.listdir(path_src) if 'ADNI' in i]:
        shutil.move(path_src+'/'+val, path_projects+'/'+dir_name+'/'+val)
f_2cp = dir_name+'.zip'

os.system('zip -q -r '+f_2cp+' '+dir_name)


client = paramiko.SSHClient()
host_keys = client.load_system_host_keys()
client.connect(HOST, username=username, password=mot_de_pass)



ls_copy_error = list()

sftp = client.open_sftp()
size_src = os.path.getsize(path_projects+'/'+f_2cp)
os.system('scp '+path_projects+'/'+f_2cp+' '+username+'@'+HOST+':'+path_dst)

size_dst = sftp.stat(path_dst+'/'+f_2cp).st_size

if size_dst != size_src:
        print('        copy error')
        ls_copy_error.append(f_2cp)
else:
        os.remove(path_src+'/'+f_2cp)
client.close()

print('copy error: ',ls_copy_error)
with open(path_log,'w') as f:
        for val in ls_copy_error:
                f.write(val+'\n')
