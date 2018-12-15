## Initialize - Generate chromosome
"""
input: midi sequence (16 sec ~ 4 phrases)
- shift_note
- merge_duplicate_note
- extend_duration
"""
import mido
from mido import Message, MidiFile, MidiTrack
import copy
from collections import Counter

 # 移調
def shift_note(song, interval):
    temp = copy.deepcopy(song)
    for i in range(len(temp)):
        temp[i].note = temp[i].note + interval
    return temp

 # 重複的切分音直接轉為連音
def merge_duplicate_note(song): 
    temp = copy.deepcopy(song)
    i=0
    while i < int(len(temp)/2)-2:
        if temp[i].note == temp[2+i].note and i%2 != 0:
            temp[i+2].time = temp[i+2].time + temp[i].time
            del(temp[i])
            del(temp[i])
            i=0
        i=i+1
    return temp

 # 延長長度過短的音
def extend_duration(song):
    # get threshold
    duration_list = []
    for i in range(len(song)):
        duration_list.append(song[i].time)
        max_freq = Counter(duration_list).most_common()[0][0]
        threshold = max_freq  if max_freq != 1 else Counter(duration_list).most_common()[1][0] ##??? midi FORMMAT不太一樣要再看看
    print(threshold)    
    # extend the duration of the note    
    temp = copy.deepcopy(song)
    for i in range(len(song)):
        if temp[i].time < threshold and temp[i].velocity == 0:
#             print(i)
            temp[i].time = threshold
    return temp
   
    
    # ## 移除過短的音
# def remove_short_note(song):
    
#     return 

# # def change_tempo(song, tempo):

# ## 增加裝飾音
# def add_note(song, position, interval):
    
#     return
