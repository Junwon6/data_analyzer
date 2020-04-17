from matplotlib import pyplot as plt
import numpy as np
import csv
import os

import zTime as time
import config

def drawGraph(path, file_name, data_type):
    data = []

    with open(path, 'r') as f:
        reader = csv.reader(f)

        for txt in reader:
            data.append(float(txt[0]))

    x = np.arange(1, len(data[2:]) + 1)
    y = np.array(data[2:])

    plt.plot(x, y)
    plt.title(time.getTime(file_name) + '(' + data_type + ')')
    plt.show()


def saveGraph(path, file_name, user_id, data_type):
    try:
        save_path = config.SAVE_PATH + '/' + user_id + '/' + data_type
        data = []
        with open(path, 'r') as f:
            reader = csv.reader(f)

            for txt in reader:
                data.append(float(txt[0]))

        x = np.arange(1, len(data[2:]) + 1)
        y = np.array(data[2:])

        plt.plot(x, y)
        plt.title(time.getTime(file_name) + '(' + data_type + ')')

        save_file_name = data_type + '_' + file_name + '.png'
        plt.savefig(os.path.join(save_path, save_file_name))
        plt.clf()
    except:
        print('fail')
    

