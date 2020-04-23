import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import config
from zFeature import getFeatures, getBVPfeatures
from zFile import getFileList

user_id = config.USER_ID[0]
dir_path = os.path.join(config.SAVE_PATH, user_id)
file_list = getFileList(dir_path)

columns = [
    'day',
    'x_med', 'x_mean', 'x_std', 'x_1q', 'x_3q', 'x_outliers', 'x_peakmean', 'x_peakvar',
    'y_med', 'y_mean', 'y_std', 'y_1q', 'y_3q', 'y_outliers', 'y_peakmean', 'y_peakvar',
    'z_med', 'z_mean', 'z_std', 'z_1q', 'z_3q', 'z_outliers', 'z_peakmean', 'z_peakvar',
    'eda_med', 'eda_mean', 'eda_std', 'eda_1q', 'eda_3q', 'eda_outliers', 'eda_peakmean', 'eda_peakvar',
    'hr_med', 'hr_mean', 'hr_std', 'hr_1q', 'hr_3q', 'hr_outliers', 'hr_peakmean', 'hr_peakvar',
    'temp_med', 'temp_mean', 'temp_std', 'temp_1q', 'temp_3q', 'temp_outliers', 'temp_peakmean', 'temp_peakvar',
    'bvp_med', 'bvp_mean', 'bvp_std', 'bvp_1q', 'bvp_3q', 'bvp_outliers', 'bvp_peakmean', 'bvp_peakvar',
    'T_c', 'T_s', 'T_d', 'T_steepest', 'T_sysToDia', 'T_dianotch', 'T_diaToEnd', 'ratio_sis_div_dia', 'ratio_dia_div_sis'
    ]

data_array = []
cnt = 0
for file_name in file_list:
    data = pd.read_csv(os.path.join(dir_path, file_name))
    day = file_name.split("_")[1][4:6] + '-' + file_name.split("_")[1][6:] + '-' + file_name.split("_")[1][2:4]

    acc_x = data['acc_x'].dropna(axis=0)
    acc_y = data['acc_y'].dropna(axis=0)
    acc_z = data['acc_z'].dropna(axis=0)
    eda = data['eda'].dropna(axis=0)
    hr = data['hr'].dropna(axis=0)
    temp = data['temp'].dropna(axis=0)
    bvp = data['bvp'].dropna(axis=0)

    acc_x_features = getFeatures(acc_x)
    acc_y_features = getFeatures(acc_y)
    acc_z_features = getFeatures(acc_z)
    eda_features = getFeatures(eda)
    hr_features = getFeatures(hr)
    temp_features = getFeatures(temp)
    bvp_features = getBVPfeatures(bvp)
    
    data_array.append([day] + acc_x_features + acc_y_features + acc_z_features + eda_features + hr_features + temp_features + bvp_features)

    cnt += 1
    if cnt == 2:
        break

df = pd.DataFrame(columns=columns,data=data_array)

df.to_csv(os.path.join(dir_path, f'{user_id}_features.csv'),index=False)