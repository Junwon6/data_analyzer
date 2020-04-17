1. extract directory name
    path : ./EldersData/[person_id]/[timestamp]_[person_id]
    content : ACC, BVP, EDA, HR, IBI, TEMP (csv files)
    
2. read file
    ACC : 3 values
    other files : 1 values

3. plot graph (save image)
    (1) plot per day
    (2) plot average per day



------------------------------------------------------
[Reshape per date]

(data)  times   degree
ACC     32      3
EDA     4       1
TEMP    4       1
BVP     64      1
HR      1       1

table
idx time bvp acc_x acc_y acc_z eda hr temp

idx     : row index
time    : 1/64 per row

1. get file list
2. filter to date (date file list)
3. make file [target_id]_[date]_total.csv
4. get file data (ACC, BVP, EDA, HR, TEMP)
5. write data