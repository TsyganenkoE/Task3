"""Vox_Celeb2_Test Threading"""
import os
import concurrent.futures
import librosa
import numpy as np

FILE_EXTENSION = ".wav"
RESULT = 'RESULT'

def result_name(filename, length):
    """Make name of the new file"""
    counter = 0
    string = []
    for i in filename:
        if counter == len(filename)-length:
            break
        string.append(i)
        counter += 1
    res_name = ''.join(string)
    return res_name

def current_dir(dir_struct, current_path):
    """Make dir list"""
    if os.path.isfile(current_path):
        return
    dir_list = os.listdir(current_path)
    for i in dir_list:
        if i[-4:] == FILE_EXTENSION:
            dir_struct.append(current_path+'/'+i)
        elif os.path.isdir(current_path+'/'+i):
            current_dir(dir_struct, current_path+'/'+i)
    return dir_struct

def get_mfcc(filename):
    """Load file , get mfcc and make file in dir with numpy result"""
    time_s, sempling_rate = librosa.load(filename)
    res = np.empty(0)
    res = librosa.feature.mfcc(time_s, sempling_rate)
    res_name = result_name(filename, 4)
    res_name = res_name[1:]
    if not os.path.exists('./'+RESULT+result_name(filename[1:], 9)):
        os.makedirs('./'+RESULT+result_name(filename[1:], 9))
    np.save('./'+RESULT+res_name, res)

dir_struct = []
dir_struct = current_dir(dir_struct, '.')
if not os.path.exists(RESULT):
    os.mkdir(RESULT, mode=0o777, dir_fd=None)
if len(dir_struct) == 0:
    exit(0)
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_mfcc, dir_struct)
