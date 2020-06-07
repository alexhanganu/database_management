# 2020-05-27

'''
ADNI/PPMI data is downloaded in a zip file and all files can be put in the list:
definition_databases.downloaded_zip_files
if not, the list of files will be considered all files present in the folder
path_zip

This script extracts the contents of each ADNI zip file, detects the subjects (based on the pos variable)
removes the MRI sequences (folders) described in dir_cleaning.terms_2_rm
and archives back each subject with the name ADNI_NAME

if definitions_adni.ls_subjids - is provided (which includes the names of the Subject_ID to be extracted)
the script will search for that Subject_ID in all downloaded_zip_files and will extract that specific Subject_ID
Alternatively, if definition_adni.ADNI_subjects is completed (a dictionary in which ADNI zip files are provided with corresponding Subject_ID)
the script will search the specific Subject_ID in the ADNI_subjects dictionary.


consider using pigz to archive with 4 cores:
tar -vc --use-compress-program="pigz -p 4" -f dir.tar.gz dir_to_tar

'''



db_name = 'ADNI'
pos = 1 #position of the dirs in the path that will differentiate the entries, e.g. dir1/dir2/dir3/... dir2 is in position 1 and for the ADNI database this corresponds to Subject_ID

path_zip = '/media/disk7/db_adni/source/mri_zipped_big' # path were are located the downloaded zip files from the ADNI/PPMI database
path_unzipped = '/media/disk7/db_adni/source/mri_unzipped' # path where the unzipped folders will be extracted
path_2_source = path_unzipped+'/'+db_name # the data from the ADNI/PPMI database are extracted to the ADNI/PPMI folder. This variable is used to search inside that ADNI folder

path_re_zip = '/media/disk7/db_adni/source/mri_zipped'#'/media/disk7/db_adni/source/mri_zipped' # this is the folder where the individual subjects archives will be put
# new_zip_file_name = db_name+'_'+Subject_ID+'.zip'

clean = True # True, if the Subject_ID folder needs to be cleaned from the MRIs that are not necessary. The MRIs that will be deleted are described in dir_cleaning.py


import zipfile
import os
import dir_cleaning



def read_zip(path, file):

	return zipfile.ZipFile(path+'/'+file, 'r')


def read_file_content(zip_f):

	return zip_f.namelist()


def xtrct_dirs(zip_f, _ls_content, path_2_unarchive):

	for val in _ls_content:

		try:
			zip_f.extract(val, path=path_2_unarchive)
		except zipfile.BadZipFile as e:
			print(e)
			pass
		except OSError as e:
			print(e)



def get_ids_content(content, _id_def):

		_id_content = dict()
		_ids = list()
		for val in content:
			_id = val.split('/')[pos]
			if not _id_def:
				if _id not in _id_content:
					_id_content[_id] = list()
					_ids.append(_id)
				_id_content[_id].append(val)
			elif _id in _id_def:
				if _id not in _id_content:
					_id_content[_id] = list()
					_ids.append(_id)
				_id_content[_id].append(val)
		return _id_content



def zip_file_archive(path, subDIR, path_re_zip):

		# changing working directory to ziped folder path
		os.chdir(path)
		path2start = os.getcwd()

		# creating the archive
		zip_f_name = path_re_zip+'/'+subDIR+'.zip'
		zip_f = zipfile.ZipFile(zip_f_name, 'w', zipfile.ZIP_DEFLATED)

		try:
			print('adding ', subDIR,' to archive')
			for root,dirs,files in os.walk(subDIR):
				for file in files:
					zip_f.write(os.path.join(root, file))
		finally:
			print('archiving finished')
			zip_f.close()




try:
	from definitions_databases import downloaded_zip_files
except ImportError:
	 	print('list of downloaded files is missing')
	 	print('files that will be used are:')
	 	downloaded_zip_files = [i for i in os.listdir(path_zip) if '.zip' in i]
print(downloaded_zip_files)
try:
	from definitions_databases import ls_subjids
	_ls_of_ids = ls_subjids
except ImportError:
	print('no list of subjects provided')
	_ls_of_ids = []


d_archived_big_files = dict()
for archive_big in downloaded_zip_files:
	d_archived_big_files[archive_big] = dict()
	zip_f = read_zip(path_zip, archive_big)
	zif_f_content = read_file_content(zip_f)
	_d_ids_content = get_ids_content(zif_f_content, _ls_of_ids)
	d_archived_big_files[archive_big] = _d_ids_content

# for key in d_archived_big_files:
# 	print(key)
# 	for subkey in d_archived_big_files[key]:
# 		print(subkey)

if not _ls_of_ids:
	_ls_of_ids = list()
	for archive_big in d_archived_big_files:
		for k in [i for i in d_archived_big_files[archive_big]]:
			_ls_of_ids.append(k)

print(_ls_of_ids)
for _subject_id in _ls_of_ids:
	new_zip_file_name = db_name+'_'+_subject_id+'.zip' # new_zip_file_name
	if new_zip_file_name not in os.listdir(path_re_zip):
		archive_big = [i for i in d_archived_big_files if _subject_id in d_archived_big_files[i]][0]
		zip_f = read_zip(path_zip, archive_big)
		print('extracting: ',_subject_id)
		xtrct_dirs(zip_f, d_archived_big_files[archive_big][_subject_id], path_unzipped)

		DIR_name = _subject_id

		if clean:
			dir_cleaning.CleanDirs(path_2_source, DIR_name)
			if db_name not in DIR_name:
				os.rename(path_2_source+'/'+DIR_name, path_2_source+'/'+db_name+'_'+DIR_name)
				DIR_name = db_name+'_'+DIR_name

		zip_file_archive(path_2_source, DIR_name, path_re_zip)

		if os.path.exists(path_re_zip+'/'+new_zip_file_name):
			print('ok to remove unzipped ', DIR_name)
			dir_cleaning.rm_dir(path_2_source+'/'+DIR_name)
	else:
		print(new_zip_file_name, ' was extracted and zipped')
