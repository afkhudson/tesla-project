import pandas as pd
import glob
import time
import os
from datetime import date

today = date.today()
d4 = today.strftime("%Y%m%d")

#data directories
tesla_ms_dir = "tesla_ms/*"
tesla_m3_dir = "tesla_m3/*"
tesla_mx_dir = "tesla_mx/*"
tesla_my_dir = "tesla_my/*"
carvana_dir = "carvana/*"
vroom_dir = "vroom/*"
shift_dir = "shift/*"

#grouping folders
check_folders = [tesla_ms_dir, tesla_m3_dir, tesla_mx_dir, tesla_my_dir, carvana_dir, vroom_dir, shift_dir]

all_data = []

#getting last updated per folder
for folder in check_folders:
    tesla_latest = max(glob.glob(folder), key=os.path.getctime)
    df = pd.read_excel(tesla_latest)
    print(f'{folder} last update: {time.ctime(os.path.getmtime(tesla_latest))}')
    print(f'lines in file: {len(df)}')
    print('-------------------------------')

input("----------------PRESS ANY BUTTON TO CONITNUE")

#creating dataframe for each file and appending to master dataframe
def get_data(dir):
    tesla_list_of_files = glob.glob(dir)
    tesla_latest = max(tesla_list_of_files, key=os.path.getctime)
    print(f'tesla_latest created: {time.ctime(os.path.getmtime(tesla_latest))}')
    df = pd.read_excel(open(tesla_latest,'rb'))
    all_data.append(df)

#running function for each folders
for folder in check_folders:
    get_data(folder)

def label_marketplace(row):
    if str(row['url']).find("tesla.com") > 0:
        return 'Tesla'
    if row['url'].find("carvana.com") > 0:
        return 'Carvana'
    if row['url'].find("shift.com") > 0:
        return 'Shift'
    if row['url'].find("vroom.com") > 0:
        return 'Vroom'

def label_avail(row):
    if row['status'].lower() == "available" or row['status'].lower() == "available now" or row['status'].lower() == "great deal" or row['status'].lower() == "2-day delivery":
        return "Available Now"
    if row['status'].lower() == "preorder" or row['status'].lower() == "available soon" or row['status'].lower() == "coming soon":
        return "Pre-Order"
    if row['status'].lower() == "locked" or row['status'].lower() == "onhold" or row['status'].lower() == "sale pending":
        return "On Hold"

all_data = pd.concat(all_data)
all_data = all_data[all_data['url'] != 'error']
all_data.apply (lambda row: label_marketplace(row), axis=1)
all_data['marketplace'] = all_data.apply (lambda row: label_marketplace(row), axis=1)
all_data.apply (lambda row: label_avail(row), axis = 1)
all_data['avail'] = all_data.apply (lambda row: label_avail(row),axis = 1)
print(all_data)

all_data.to_csv(f'all_data/{d4} all data.csv', index=False)
