import os
import paramiko

r_HOST_src = 'mp2.calculcanada.ca'
r_username_src = 'hanganua'
r_mot_de_pass_src = 'iugm@Pass8'
path_src = '/home/hanganua/projects/def-hanganua/adni/source/mri_unzipped'



r_HOST_dst = 'beluga.calculquebec.ca'
r_username_dst = 'hanganua'
r_mot_de_pass_dst = 'iugm@Pass8'
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

ls_miss = ['002_S_4219', '002_S_4225', '002_S_4251', '002_S_4270', '005_S_0610', '006_S_0498', '012_S_4026', '013_S_1186', '013_S_4268', '016_S_4009', '018_S_4257', '019_S_4252', '021_S_4245', '027_S_0074', '031_S_4021', '032_S_0677', '035_S_0156', '037_S_0303', '037_S_0377', '037_S_0454', '037_S_4028', '037_S_4214', '041_S_0679', '041_S_4271', '052_S_0671', '053_S_2396', '057_S_2398', '082_S_1256', '098_S_4018', '098_S_4275', '114_S_0416', '116_S_0649', '123_S_1300', '126_S_2407', '127_S_1427', '131_S_0384', '136_S_0186', '141_S_1378', '941_S_1195']