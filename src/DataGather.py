import requests
import zipfile
import os

base_url = "https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/"
years = range(2018, 2019)
quarters = ["q1", "q2", "q3", "q4"]

for year in years:
    for quarter in quarters:
        name = str(year) + quarter
        url = base_url + name + "_notes.zip"
        r = requests.get(url)
        file_addr = '../data/' + name + '.zip'
        with open(file_addr, 'wb') as f:
            f.write(r.content)
            with zipfile.ZipFile(file_addr, 'r') as zip:
                zip.extractall('../data/' + name + '/')
# TODO: Delete .zip files after extraction?
                # os.remove(file_addr)

# example
# https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/2019q3_notes.zip