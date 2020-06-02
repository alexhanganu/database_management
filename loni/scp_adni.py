'''
2020-05-28

script aims to copy from local to remote computer
the folders that are not present in the specified remote folder

'''

path_src = '/media/ssp/db_cog/db_adni/source/mri_zipped' # path to the local folder that contains the files or folders to be copied
path_log = '/home/ssp/Desktop/log.txt' # path on the local computer where a log file will be stored that will contain the folders that were not copied correctly
path_dst_dir = 'projects/def-hanganua/adni/source/mri_zipped' 
path_credentials = '/home/ssp/' # path to the txt-like file named "credentials" that will contain the following data:

'''
username = 'string' # username to access the remote computer
mot_de_pass = 'string' # password to access the remote computer
HOST = 'name.address.com' # host name of the remote computer
'''


import os
import paramiko
import shutil

shutil.copy(path_credentials+'/credentials', os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
try:
	from credentials import username, mot_de_pass, HOST
	os.remove(os.path.dirname(os.path.abspath(__file__))+'/credentials.py')
except ImportError:
	print('file with credentials was not found')
	raise SystemExit()

path_dst = '/home/'+username+'/'+path_dst_dir # path to the remote folder that the files/ folders will be copied to

client = paramiko.SSHClient()
host_keys = client.load_system_host_keys()
client.connect(HOST, username=username, password=mot_de_pass)
stdin, stdout, stderr = client.exec_command('ls '+path_dst)

ls_src = os.listdir(path_src)

ls_dst = list()
for line in stdout:
	ls_dst.append(line.strip('\n'))

ls_copy = [i for i in ls_src if i not in ls_dst]


print('left to copy: ',len(ls_copy),' subjects')
print('estimated time to copy: ',len(ls_copy)*10/60,' hours')

ls_copy_error = list()

sftp = client.open_sftp()
for val in ls_copy:
	size_src = os.path.getsize(path_src+'/'+val)
	print(val, size_src)
	# sftp.put(path_src+'/'+val, path_dst)
	os.system('scp '+path_src+'/'+val+' '+username+'@'+HOST+':'+path_dst)

	size_dst = sftp.stat(path_dst+'/'+val).st_size

	if size_dst != size_src:
		print('        copy error')
		ls_copy_error.append(val)

client.close()

print('copy error: ',ls_copy_error)
with open(path_log,'w') as f:
	for val in ls_copy_error:
		f.write(val+'\n')
