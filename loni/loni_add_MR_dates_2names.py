dates_file = 'recon_dates.json'

src_fsdata = '/scratch/hanganua/database/loni_adni/processed_fs'


from os import listdir, system, path
import json

def get_dates():
    with open(dates_file) as jf:
        return json.load(jf)


def change_name(subjid, ls, date):
    zipf = subjid+'.zip'
    if zipf in ls:
        print('mv '+path.join(src_fsdata, zipf)+' '+path.join(src_fsdata, zipf.strip('.zip')+'_'+date+'.zip'))
        system('mv '+path.join(src_fsdata, zipf)+' '+path.join(src_fsdata, zipf.strip('.zip')+'_'+date+'.zip'))
    else:
        print(zipf,' missing')


dates = get_dates()
ls = listdir(src_fsdata)

for subjid in dates:
    change_name(subjid, ls, dates[subjid][0][0][:10])
