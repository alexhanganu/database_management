import os
import paramiko

r_HOST_src = 'mp2.calculcanada.ca'
r_username_src = 'hanganua'
r_mot_de_pass_src = ''
path_src = '/home/hanganua/projects/def-hanganua/adni/source/mri_unzipped'



r_HOST_dst = 'beluga.calculquebec.ca'
r_username_dst = 'hanganua'
r_mot_de_pass_dst = ''
path_dst = '/scratch/'+r_username_dst+'/mri_unzipped'

client1 = paramiko.SSHClient()
host_keys = client1.load_system_host_keys()

client1.connect(r_HOST_src, username=r_username_src, password=r_mot_de_pass_src)
stdin, stdout1, stderr = client1.exec_command('ls '+path_src)

src_size = list()
for line in stdout1:
	subjid = line.strip('\n')
	src_size.append(subjid)




client2 = paramiko.SSHClient()
host_keys = client2.load_system_host_keys()

client2.connect(r_HOST_dst, username=r_username_dst, password=r_mot_de_pass_dst)

stdin, stdout2, stderr = client2.exec_command('ls '+path_dst)

dst_size = list()
for line in stdout2:
	subjid = line.strip('\n')
	dst_size.append(subjid)





ls_copy = [i for i in dst_size if src_size[i] != dst_size[i]]
print(ls_copy)

ls_miss = [i for i in src_size if i not in dst_size]
print(ls_miss)

