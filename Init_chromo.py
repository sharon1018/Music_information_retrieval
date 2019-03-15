## Initialize - Generate chromosome
"""
input: midi sequence (4 bar)
- shift_note
- merge_duplicate_note
- extend_duration
- add_note
- delete_note
"""

import mido
import numpy as np
from mido import Message, MidiFile, MidiTrack
import copy
from collections import Counter
import random

 # 移調
def shift_note(song, interval):
    temp = copy.deepcopy(song)
    return [temp[i].note + interval for i in range(len(temp))]

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
    duration_list = [song[i].time for i in range(len(song))]
    # extend the duration of the note    
    temp = copy.deepcopy(song)
    count = 0
    for i in range(len(song)-1):
        if temp[i].velocity != 0 and temp[i].time + temp[i+1].time == src:
            if count <= MAX:
                temp[i+1].time = trgt - temp[i].time
                count += 1
    return temp

# 決定裝飾音
def get_note(note):
    choice_list = [4, 3, -3, -4, 2, -2, 1, -1]
    if note % 12 == 0: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.25, 0, 0.25, 0, 0.25, 0, 0, 0.25])
    elif note % 12 == 2: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0, 0.25, 0.25, 0, 0.25, 0.25, 0, 0])
    elif note % 12 == 4: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0, 0.25, 0, 0.25, 0, 0.25, 0.25, 0])
    elif note % 12 == 5: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.25, 0, 0.25, 0, 0.25, 0, 0, 0.25])
    elif note % 12 == 7: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.25, 0, 0.25, 0, 0.25, 0.25, 0, 0])
    elif note % 12 == 9: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0, 0.25, 0, 0.25, 0.25, 0.25, 0, 0])
    elif note % 12 == 11: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0, 0.25, 0, 0.25, 0, 0.25, 0.25, 0])
    else:
        change_note = 0
    return int(change_note)

 # 增加裝飾音
def add_note(song, duration, num):
    temp = copy.deepcopy(song)
    for i in range(num):
        position = 1 # initial
        while position % 2 != 0:
            position = random.randint(0,len(temp)-1)
        _note = temp[position].note
        interval = get_note(_note)
        print(interval)
        if interval != 0:
            temp.insert(position, (mido.Message('note_on', velocity = 100, note = _note + interval , time = 1)))
            temp.insert(position + 1, (mido.Message('note_on', velocity = 0, note = _note + interval, time = duration)))
            temp[i+position+3].time -= duration  # 下個音時間要減短    
    return temp
# 移除某些音
def remove_note(song, delete_threshold):
    temp = copy.deepcopy(song)
    position = 1
    while position % 2 != 0 and temp[position+1].time < delete_threshold:
        position = random.randint(0,len(temp)-1)
    temp[position-1].time += (temp[position+1].time + temp[position].time)
    del temp[position]
    del temp[position]
    return temp