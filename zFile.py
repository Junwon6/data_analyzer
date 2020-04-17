import os
import config
import zTime as time

def getFileList(dir_name):
    file_names = os.listdir(dir_name)
    file_names.sort()

    return list(filter(lambda file_name: file_name[0] != '.', file_names))


def getCSVFileList(dir_name):
    temp_list = []

    file_names = os.listdir(dir_name)
    file_names.sort()

    for file_name in file_names:
        ext = os.path.splitext(file_name)[-1]
        if ext == '.csv':
            temp_list.append(file_name)

    return temp_list


def makeDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def initSaveDirectory(save_path):
    makeDirectory(save_path)
    data_types = config.DATA_TYPE

    for data_type in data_types:
        dir_path = os.path.join(save_path, data_type)
        makeDirectory(dir_path)


def getFileInfo(user_id):
    dir_path = os.path.join(config.PATH, user_id)
    file_list = getFileList(dir_path)

    data_types = config.DATA_TYPE
    file_count = {}

    for data_type in data_types:
        file_count[data_type] = 0
    
    for file_name in file_list:
        full_path = os.path.join(dir_path, file_name)
        csv_files = getCSVFileList(full_path)

        for data_type in data_types:
            if (data_type + '.csv') in csv_files:
                file_count[data_type] += 1
    return file_count


def getCount(user_id):
    user_file_count = getFileInfo(user_id)

    total_count = sum(user_file_count.values()) - user_file_count['ACC']
    currrent_count = 0

    return total_count, currrent_count

def getDateList(user_id):
    dir_path = os.path.join(config.PATH, user_id)
    file_list = getFileList(dir_path)

    date_list = []
    for file_name in file_list:
        date = time.getDate(file_name)
        print(date)

# getDateList()
# def matchFile(user_id):
#     file_list = []

#     dir_path = os.path.join(config.PATH, user_id)
#     file_list = getFileList(dir_path)

#     data_types = config.DATA_TYPE

#     for file_name in file_list:
#         full_path = os.path.join(dir_path, file_name)
#         csv_files = getCSVFileList(full_path)

#         for data_type in data_types:
#             if data_type == 'ACC':
#                 continue
#             if (data_type + '.csv') in csv_files:
#                 file_list.append(data_type + '_' + file_name + '.png')

#     save_path = os.path.join(config.SAVE_PATH, user_id)
#     for data_type in data_types:
#         if data_type == 'ACC':
#             continue
#         save_file_list = getFileList(os.path.join(save_path, data_type))
#         print(save_file_list)
#         for save_file in save_file_list:
#             if save_file in file_list:
#                 file_list.pop(file_list.index(save_file))

# matchFile('A01AC9')