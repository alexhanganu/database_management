# 2020-05-21
'''
zip files downloaded from the ADNI database have many MRI sequences that are not needed for the analysis.
This script searches each Subject_ID folder for the sequences described in 
terms_2_rm
and removes those folders
this allows to diminish the size of the stored data and also keep only the sequences that are needed
'''


import os, shutil

terms_2_rm = ['calibration','loc','scout','relCBF','cerebral_blood_flow','asset','survey',
			'3D_PASL','3d_pcasl','tgse_pcasl','axial_2d_pasl','double_tse','sPWI','fcmri',
			'average_dc','isotropic_image','Perfusion_Weighted','ASL_PERFUSION',
			'T2_TSE','t2-tse','t2_fse','t2-fse','pd_t2','pd-t2','8hrbrain','fgre',
			'take_off_auto_send','fractional_aniso','fractional_ansio'] #list of terms that if present in the content - will be removed


class CleanDirs():

	def __init__(self, path_DIRS, subDIR):

		ls_2rm, ls_2keep = self.get_ls2rm(path_DIRS, subDIR)
		print('keeping: ',ls_2keep)
		self.rm_terms(ls_2rm, path_DIRS, subDIR)


	def get_ls2rm(self, path_DIRS, subDIR):

		print('checking ',subDIR)
		ls_init = os.listdir(path_DIRS+'/'+subDIR)
		ls_2rm = list()
		for val in ls_init:
			for val2chk in terms_2_rm:
				if val2chk.lower() in val.lower():
					ls_2rm.append(val)
					break
		ls_2keep = [i for i in ls_init if i not in ls_2rm]
		return ls_2rm, ls_2keep


	def rm_terms(self, ls_2rm, path_DIRS, subDIR):

		for val in ls_2rm[::-1]:
			rm_dir(path_DIRS+'/'+subDIR+'/'+val)
			# print('    removing ',path_DIRS+'/'+subDIR+'/'+val)
			# shutil.rmtree(path_DIRS+'/'+subDIR+'/'+val)


def rm_dir(path_dir):

		print('    removing ',path_dir)
		shutil.rmtree(path_dir)


def cp_f(path_src, path_dst):
	shutil.copy(path_src, path_dst)

