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
    print(f'{folder} last update: {time.ctime(os.path.getmtime(tesla_latest))}')

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

all_data = pd.concat(all_data)
print(all_data)
all_data.to_csv(f'all_data/{d4} all data.csv', index=False)
