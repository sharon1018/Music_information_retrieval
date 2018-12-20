## Initialize - Generate chromosome
"""
input: midi sequence (4 bar)
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
def change_duration(song, src, trgt, MAX): # one beat = 480
    # get threshold
    duration_list = []
    for i in range(len(song)):
        duration_list.append(song[i].time)
    # # extend the duration of the note    
    temp = copy.deepcopy(song)
    count = 0
    for i in range(len(song)-1):
        if temp[i].velocity != 0 and temp[i].time + temp[i+1].time == src:
            if count <= MAX:
                temp[i+1].time = trgt - temp[i].time
                count += 1
    return temp
   
    
    # ## 移除過短的音
# def remove_short_note(song):
    
#     return 

# # def change_tempo(song, tempo):

# ## 增加裝飾音
# def add_note(song, position, interval):
    
#     return
