#!/bin/python
#2020 06 19

'''
extract stats
zip subjects in subjects_processed
after that is necessary to zip the processed_fs_stats and move it to the corresponding
storage folder (i.e., for ADNI is beluga../projects/../adni)
'''
HOST = 'beluga.calculquebec.ca'
'''
username = 'string' # username to access the remote computer
mot_de_pass = 'string' # password to access the remote computer
HOST = 'name.address.com' # host name of the remote computer
'''


from os import listdir, system, mkdir, path, chdir, getuid, getenv
import shutil, getpass, time

environ['TZ'] = 'US/Eastern'
time.tzset()
    dthm = time.strftime('%Y/%m/%d %H:%M')

def get_username():
    username = ''
    try:
        import pwd
        username = pwd.getpwuid( getuid() ) [0]
    except ImportError:
        print(e)
    if not username:
    	try:
    		import getpass
    		username = getpass.getuse()
    	except ImportError:
    		print('getpass not installed')
    if not username:
    	try:
            if user in getenv('HOME'):
                username = user
                break
    return username

username = getpass.getuser()
path_credentials = os.path.join('/home',username) # path to the txt-like file named "credentials" that will contain the follow$




path_projects = path.join('/home',username,'projects','def-hanganua')
path_scratch = path.join('/scratch',username)
path_processed = path.join(path_projects,'subjects_processed')

dir_stats = 'processed_fs_stats'
zip_f = dir_stats+'_'+dthm+'.zip'

path_dst_dir_adni = os.path.join('adni','processed_fs') # on beluga
path_dst_dir_ppmi = os.path.join('ppmi','processed_fs') # on elm

path_dst_dir = path_dst_dir_adni
path_src = os.path.join(path_projects,'subjects_processed') # path that contains the files or folders t$
path_log = os.path.join(path_projects,'scripts','scp_log.txt') # path where a log file will be stored tha$
path_dst = os.path.join(path_projects,path_dst_dir) # path to the remote folder that the files/ folders w$





path_stats = path.join(path_scratch,dir_stats)


chdir(path_processed)

if not path.exists(path_stats):
    mkdir(path_stats)

stats_dirs = listdir(path_stats)

for subDIR in listdir(path_processed):
    if path.isdir(path.join(path_processed, subDIR)) and subDIR not in stats_dirs:
        print('extracting stats')
        mkdir(path_stats+'/'+subDIR)
        shutil.copytree(path.join(path_processed,subDIR,'stats'),path.join(path_stats,subDIR,'stats'))
        print('archiving ',subDIR)
        system('zip -q -r -m '+subDIR+'.zip '+subDIR)
    elif not path.isdir(path.join(path_processed, subDIR)):
        print(subDIR, ' not a directory')

chdir(path_scratch)
system('zip -q -r -m '+zip_f+' '+dir_stats)
shutil.move(path.join(path_scratch,zip_f), path.join(path_processed,zip_f))




# following scripts will copy from the local remote to the HOST remote at the path_dst path

shutil.copy(os.path.join(path_credentials,'credentials'), os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
try:
        from credentials import mot_de_pass
        os.remove(os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
except ImportError:
        print('file with credentials was not found')
        raise SystemExit()



# setting up the remote connection
#  retrieving the list of files in the destination folder
client = paramiko.SSHClient()
host_keys = client.load_system_host_keys()
client.connect(HOST, username=username, password=mot_de_pass)
stdin, stdout, stderr = client.exec_command('ls '+path_dst)

# retrieving the list of files in the source folder
ls_src = [i for i in os.listdir(path_src) if '.zip' in i]

ls_dst = list()
for line in stdout:
        ls_dst.append(line.strip('\n'))

# retrieving the list of folders that are absent in the destination folder and need to be copied
ls_copy = [i for i in ls_src if i not in ls_dst]
print('left to copy: ',len(ls_copy),' subjects')



# copying the files 
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