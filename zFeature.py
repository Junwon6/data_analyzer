import numpy as np
from scipy.signal import find_peaks
import scipy

def countOutliers(x,mean,sigma):
    outliers = 0
    for i in x:
        if (i > (mean + 2*sigma)) or (i<(mean-2*sigma)):
            outliers = outliers+1
        else:
            continue
    return outliers

def getFeatures(x):
    if len(x) == 0:
        return [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    result = list()
    median = np.median(x)
    result.append(median) #median
    mean = np.mean(x)
    result.append(mean)  #mean
    std = np.std(x)
    result.append(std)  #standard deviation
    result.append(np.percentile(x,25)) #1-quartile
    result.append(np.percentile(x,75)) #3-quartile
    outliers = countOutliers(x,mean,std) 
    result.append(outliers)     # number of outliers
    
    x_peak = scipy.signal.find_peaks(x)
    peaks = x_peak[0]
    if len(peaks) == 0:
        peak_mean = np.nan
        peak_var = np.nan
    else:
        peak_mean = np.mean(peaks)
        peak_var = np.var(peaks)
    result.append(peak_mean)  # mean of peaks
    result.append(peak_var)  # variance of peaks
    return result

def getBVPfeatures(x):
    if len(x) == 0:
        return [
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan
            ]
    fs = 0.016
    result = list()
    median = np.median(x)
    result.append(median) #median
    mean = np.mean(x)
    result.append(mean)  #mean
    std = np.std(x)
    result.append(std)  #standard deviation
    result.append(np.percentile(x,25)) #1-quartile
    result.append(np.percentile(x,75)) #3-quartile
    outliers = countOutliers(x,mean,std) 
    result.append(outliers)     # number of outliers
    
    x_peak = scipy.signal.find_peaks(x)
    peaks = x_peak[0]
    peak_mean = np.mean(peaks)
    result.append(peak_mean)  # mean of peaks
    peak_var = np.var(peaks)
    result.append(peak_var)  # variance of peaks
    
    i1 = find_peaks(x, width=0)[0]
    i2 = find_peaks(-x.copy())[0]
    i3 = np.r_[i1,i2]
    i3.sort()
    
    df=x.diff()
    di1 = find_peaks(df)[0]
    
    systolic_peak = np.where(x[i3].diff()>0.1)[0]
    #T_c
    T_c=(i3[systolic_peak[1]]-i3[systolic_peak[0]])*fs
    result.append(T_c)
    #T_s
    T_s=(i3[systolic_peak[1]]-i3[systolic_peak[1]-1])*fs
    result.append(T_s)
    #T_d
    T_d=T_c-T_s
    result.append(T_d)
    #T_steepest
    T_steepest=(((di1<i3[systolic_peak[1]])*di1).max()-i3[systolic_peak[1]-1])*fs
    result.append(T_steepest)
    #T_sysToDia
    T_sysToDia=(di1[np.where(di1>i3[systolic_peak[0]])[0][0]]-i3[systolic_peak[0]])*fs
    result.append(T_sysToDia)
    #T_dianotch
    T_dianotch=T_sysToDia+T_s
    result.append(T_dianotch)
    #T_diaToEnd
    T_diaToEnd=(i3[systolic_peak[1]-1]-di1[np.where(di1>i3[systolic_peak[0]])[0][0]])*fs
    result.append(T_diaToEnd)
    #ratio_sis_dia
    ratio_sis_dia=i3[systolic_peak[0]]/i3[systolic_peak[0]+1]
    result.append(ratio_sis_dia)
    #ratio_dia_sis
    ratio_dia_sis=1/ratio_sis_dia
    result.append(ratio_dia_sis)  
    
    return result


# def getOutlierCount(df, coe_sig):
#     range_min = df.mean() - (coe_sig * df.std())
#     range_max = df.mean() + (coe_sig * df.std())

#     cnt = 0
#     for value in df:
#         if value < range_min or value > range_max:
#             cnt += 1

#     return cnt

# def getPeak(data):
#     d = data
#     t = -d.copy()
#     i1 = find_peaks(d, width=0)[0]
#     i2 = find_peaks(t)[0]
#     i3 = np.r_[i1, i2]
#     i3.sort()

#     df = d.diff()
#     di1 = find_peaks(df)[0]

#     # systolic_peak = np.where(d[i3].diff() > 0.1)[0]
#     systolic_peak = np.where(pd.DataFrame(d.values[i3]).diff() > 0.1)[0]
#     ppg_feature=pd.DataFrame()
#     try:
#         T_c = (i3[systolic_peak[1]]-i3[systolic_peak[0]])*fs
#         T_s = (i3[systolic_peak[1]]-i3[systolic_peak[1]-1])*fs
#         T_d = T_c-T_s
#         T_steepest = (((di1 < i3[systolic_peak[1]])
#                         * di1).max()-i3[systolic_peak[1]-1])*fs
#         T_sysToDia = (di1[np.where(di1 > i3[systolic_peak[0]])[
#                         0][0]]-i3[systolic_peak[0]])*fs
#         T_dianotch = T_sysToDia+T_s
#         T_diaToEnd = (i3[systolic_peak[1]-1] -
#                         di1[np.where(di1 > i3[systolic_peak[0]])[0][0]])*fs
#         ratio_sis_div_dia = i3[systolic_peak[0]]/i3[systolic_peak[0]+1]
#         ratio_dia_div_sis = 1/ratio_sis_div_dia

#         if T_steepest > 0 and T_sysToDia > 0 and T_diaToEnd > 0:
#             ppg_feature.loc[0, 'T_c'] = T_c
#             ppg_feature.loc[0, 'T_s'] = T_s
#             ppg_feature.loc[0, 'T_d'] = T_d
#             ppg_feature.loc[0, 'T_steepest'] = T_steepest
#             ppg_feature.loc[0, 'T_systodia'] = T_sysToDia
#             ppg_feature.loc[0, 'T_dianotch'] = T_dianotch
#             ppg_feature.loc[0, 'T_diatoend'] = T_diaToEnd
#             ppg_feature.loc[0, 'sys/dia'] = ratio_sis_div_dia
#             ppg_feature.loc[0, 'dia/sys'] = ratio_dia_div_sis

#         else:
#             ppg_feature.loc[0, :] = np.nan
#         return ppg_feature
#     except:
#         ppg_feature.loc[0, :] = np.nan
#         return ppg_feature
