'''
2020-06-13

script aims to copy from local to remote computer
the folders that are not present in the specified remote folder
requires paramiko. On the cluster - this cannot be installed, thus do:
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

choose yes to accept PYTHONPATH change, after the installation:
source ~/.bashrc

conda install paramiko
after that you can use the python from the miniconda, that has paramiko installed
'''
import shutil, getpass, os, paramiko
username = getpass.getuser()

HOST = 'beluga.calculquebec.ca'



path_credentials = os.path.join('/home',username) # path to the txt-like file named "credentials" that will contain the follow$

path_dst_dir_adni = os.path.join('adni','processed_fs') # on beluga
path_dst_dir_ppmi = os.path.join('ppmi','processed_fs') # on elm

path_dst_dir = path_dst_dir_adni

path_projects = os.path.join('/home',username,'projects','def-hanganua')
path_src = os.path.join(path_projects,'subjects_processed') # path that contains the files or folders t$
path_log = os.path.join(path_projects,'scripts','scp_log.txt') # path where a log file will be stored tha$
path_dst = os.path.join(path_projects,path_dst_dir) # path to the remote folder that the files/ folders w$


'''
username = 'string' # username to access the remote computer
mot_de_pass = 'string' # password to access the remote computer
HOST = 'name.address.com' # host name of the remote computer
'''



 
shutil.copy(os.path.join(path_credentials,'credentials'), os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
try:
        from credentials import mot_de_pass
        os.remove(os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
except ImportError:
        print('file with credentials was not found')
        raise SystemExit()



client = paramiko.SSHClient()
host_keys = client.load_system_host_keys()
client.connect(HOST, username=username, password=mot_de_pass)
stdin, stdout, stderr = client.exec_command('ls '+path_dst)

ls_src = [i for i in os.listdir(path_src) if '.zip' in i]

ls_dst = list()
for line in stdout:
        ls_dst.append(line.strip('\n'))

ls_copy = [i for i in ls_src if i not in ls_dst]


print('left to copy: ',len(ls_copy),' subjects')


ls_copy_error = list()

sftp = client.open_sftp()
for val in ls_copy:
        size_src = os.path.getsize(path_src+'/'+val)
        # sftp.put(path_src+'/'+val, path_dst)
        print('left to copy: ',len(ls_copy[ls_copy.index(val):]))
        os.system('scp '+path_src+'/'+val+' '+username+'@'+HOST+':'+path_dst)

        size_dst = sftp.stat(path_dst+'/'+val).st_size

        if size_dst != size_src:
                print('        copy error')
                ls_copy_error.append(val)
        else:
                os.remove(path_src+'/'+val)
client.close()

print('copy error: ',ls_copy_error)
with open(path_log,'w') as f:
        for val in ls_copy_error:
                f.write(val+'\n')
