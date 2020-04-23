import config
import zGraph as graph
import zFile as fileCalc
import zTime as time
import zFeature as feature
import os
import glob
import pandas as pd
import numpy as np

import csv

def reshape():
    user_id = config.USER_ID[0]
    save_path = os.path.join(config.SAVE_PATH, user_id)
    dir_path = os.path.join(config.PATH, user_id)

    file_list = fileCalc.getFileList(dir_path)
    date_list = list(dict.fromkeys(list(map(lambda file_name: time.getDate(file_name), file_list))))
    

    for file_name in file_list:
        date = time.getDate(file_name)
        file_path = os.path.join(dir_path, file_name)
        print(date, file_name)

        ACC = pd.read_csv(os.path.join(file_path, 'ACC.csv'), skiprows = [0, 1], names=['acc_x', 'acc_y', 'acc_z'])
        EDA = pd.read_csv(os.path.join(file_path, 'EDA.csv'), skiprows = [0, 1], names=['eda'])
        TEMP = pd.read_csv(os.path.join(file_path, 'TEMP.csv'), skiprows = [0, 1], names=['temp'])
        BVP = pd.read_csv(os.path.join(file_path, 'BVP.csv'), skiprows = [0, 1], names=['bvp'])
        HR = pd.read_csv(os.path.join(file_path, 'HR.csv'), skiprows = [0, 1], names=['hr'])

        ACC['idx'] = [int(i * 2) for i in range(0, len(ACC))]
        EDA['idx'] = [int(i * 16) for i in range(0, len(EDA))]
        TEMP['idx'] = [int(i * 16) for i in range(0, len(TEMP))]
        BVP['idx'] = range(0, len(BVP))
        HR['idx'] = [int(i * 64) for i in range(0, len(HR))]

        ACC.set_index('idx', inplace=True)
        EDA.set_index('idx', inplace=True)
        TEMP.set_index('idx', inplace=True)
        BVP.set_index('idx', inplace=True)
        HR.set_index('idx', inplace=True)

        df = BVP.join(ACC, how='outer')
        df = df.join(EDA, how='outer')
        df = df.join(HR, how='outer')
        df = df.join(TEMP, how='outer')

        df['time'] = [i * (1 / 64) for i in range(0, len(df))]

        columnsTitles = ['time', 'bvp', 'acc_x', 'acc_y', 'acc_z', 'eda', 'temp', 'hr']
        df = df.reindex(columns=columnsTitles)
        df.reset_index(drop=True, inplace=True)
        df.index = np.arange(1, len(df) + 1)

        save_file_path = os.path.join(save_path, f'{user_id}_{date}_total.csv')
        if os.path.isfile(save_file_path):
            df.to_csv(save_file_path, mode='a', na_rep='NA', header=False)
        else:
            df.to_csv(save_file_path, mode='w', na_rep='NA')
        del df




def getFeature():
    user_id = config.USER_ID[0]
    dir_path = os.path.join(config.SAVE_PATH, user_id)
    file_list = fileCalc.getFileList(dir_path)

    for file_name in file_list:
        data = pd.read_csv(os.path.join(dir_path, file_name))

        eda = {
            'eda_med': data['eda'].dropna(axis=0).median(),
            'eda_mean': data['eda'].dropna(axis=0).mean(),
            'eda_std': data['eda'].dropna(axis=0).std(),
            'eda_1q': data['eda'].dropna(axis=0).quantile(.25),
            'eda_3q': data['eda'].dropna(axis=0).quantile(.75),
            'eda_outliers': feature.getOutlierCount(data['eda'].dropna(axis=0), 2)
        }
        

        # print(eda)
        print(feature.getPeak(data['eda'].dropna(axis=0)))
        break



if __name__ == "__main__":
    getFeature()