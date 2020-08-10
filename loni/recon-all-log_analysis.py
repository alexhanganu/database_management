"""
function
extracts the dates of MRI acquisitions that were used for 
FreeSurfer processing
"""

from os import path, makedirs, listdir
import sys
import json
import datetime as dt



SUBJECTS_DIR = path.join("/scratch", "hanganua", "reconlog")


def validate_if_date(date_text):
    try:
        date = dt.datetime.strptime(date_text, '%Y-%m-%d_%H_%M_%S.%f')
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    if not path.exists(SUBJECTS_DIR):
        print(SUBJECTS_DIR, ' is missing')
        sys.exit(0)

    ids_date = dict()

    for subject in listdir(SUBJECTS_DIR):
        print("reading recon-all.log for: "+ subject)
        content = open(path.join(SUBJECTS_DIR, subject, 'scripts', 'recon-all.log'),'r').readlines()

        ids_date[subject] = [[n for n in i.split('/') if validate_if_date(n)] for i in content[:10] if '-i' in i]

    with open(path.join("/scratch", "hanganua", "recon_dates.json"),'w') as jf:
        json.dump(ids_date, jf, indent=4)
