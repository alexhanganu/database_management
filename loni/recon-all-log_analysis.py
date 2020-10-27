"""
reads recon-all.log file from FreeSurfer
reads the first registration line
: returns raw file used for registration, if param == 'raw_file'
: returns date of the raw file used for registration, if param == 'date'

extracts the dates of MRI acquisitions that were used for 
FreeSurfer processing
"""

from os import path, makedirs, listdir
import sys
import json
import datetime as dt

class FreeSurferLog_Read:
    def __init__(self, SUBJECTS_DIR, path2save_result, param):
        self.SUBJECTS_DIR = SUBJECTS_DIR
        self.save = path2save_result
        self.d = dict()

        for subject in listdir(SUBJECTS_DIR):
            print("reading recon-all.log for: "+ subject)
            self.content = self.get_log(subject)
            self.d[subject] = self.get_string_param(param)

        self.save_2json(self.d)
    
    def get_string_param(self, param):
        if param == 'date':
            return [n for n in i.split('/') if self.validate_if_date(n) for i in self.get_string_param('raw_files')]
        if param == 'raw_files':
            return [i for i in self.content[:10] if '-i' in i]

    def get_log(self, subject):
        return open(path.join(self.SUBJECTS_DIR, subject, 'scripts', 'recon-all.log'),'r').readlines()

    def validate_if_date(self, date_text):
        try:
            date = dt.datetime.strptime(date_text, '%Y-%m-%d_%H_%M_%S.%f')
            return True
        except ValueError:
            return False

    def save_2json(self, d):
        with open(path.join(self.save, 'result.json'),'w') as jf:
            json.dump(d, jf, indent=4)

if __name__ == "__main__":
    SUBJECTS_DIR = input('please provide SUBJECTS_DIR:')
    while not path.exists:
        SUBJECTS_DIR = input('path incorrent. Please provide SUBJECTS_DIR:')
    path2save_result = input('please provide path to save the results:')
    while not path.exists:
        path2save_result = input('path incorrent. Please provide path to save the results:')
    param = input('please choose between paremeters: date/ raw_files: (type parameter)')
    FreeSurferLog_Read(SUBJECTS_DIR, path2save_result, param)


