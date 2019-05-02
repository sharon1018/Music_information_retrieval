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


# 增加一個音
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


 # 延長長度過短的音 (unused)
def change_duration(song, src, trgt): # one beat = 480
    i = 0   
    temp = copy.deepcopy(song)
    while i % 2 != 0 :
        i = random.randint(0,len(song))       
    if temp[i].velocity != 0 and temp[i].time + temp[i+1].time == src:
           temp[i+1].time = temp[i].time - 60
    temp[i-3].time = temp[i+1].time + temp[i-3].time
    return temp


 # 縮短duration （unused）
def shorten_duration(song, times, duration): # one beat = 480
    for i in range(times):
        i = 0   
        temp = copy.deepcopy(song)
        while i % 2 != 0 and temp[i].velocity != 0 and temp[i].time + temp[i+1].time == duration and temp[i].note == temp[i+1].note:
            i = random.randint(0,len(song))       
            temp[i+1].time = temp[i].time - duration
    return temp


def note_series(interval, _note):
    m = [mido.Message('note_on', velocity = 100, note = _note + interval[0], time = 1),
         mido.Message('note_on', velocity = 0,   note = _note + interval[0], time = 119),
         mido.Message('note_on', velocity = 100, note = _note + interval[1], time = 1),
         mido.Message('note_on', velocity = 0,   note = _note + interval[1], time = 119),
         mido.Message('note_on', velocity = 100, note = _note + interval[2], time = 1),
         mido.Message('note_on', velocity = 0,   note = _note + interval[2], time = 119),
         mido.Message('note_on', velocity = 100, note = _note + interval[3], time = 1),
         mido.Message('note_on', velocity = 0,   note = _note + interval[3], time = 119)]
    return m
  
melody_series = [[0,-5,0,4],[0,0,0,0], [0,-8,-3,0],[0,0,0,0],[0,-9,-4,0],[0,-8,-3,0],[0,0,0,0], [0,-7,-3,0],[0,0,0,0], [0,-7,-4,0],[0,0,0,0],[0,-9,-4,0]]

melody_series2 = [[0,-1,0,2],[0,0,0,0], [0,-5,-3,0],[0,0,0,0],[0,-4,-2,0],[0,-1,-3,0],[0,0,0,0], [0,-7,-5,0],[0,0,0,0], [0,-2,0,2],[0,0,0,0],[0,-2,-4,0]]

def add_melody(song):
    position = 1
    temp = copy.deepcopy(song)

    # 將長度為四分音符的分解為4個16分音符
    while position % 2 != 0  and position < len(song)-1 and temp[position].time + temp[position+1].time < 480:
        position = int(random.randint(2,len(temp)-2))    
    _note = temp[position].note
    idx = _note % 12 
    
    # 移除選中的四分音符
    del temp[position]
    del temp[position]
    
    # 替換成4個16分音符
    interval = melody_series[idx]
    m = note_series(interval, _note)
    temp[position:position] = m 
   
    return temp



# 決定和諧音
def get_chord(note):
    choice_list = [4, 3, -3, -4]
    if note % 12 == 0: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.5,0,0.5,0])
    elif note % 12 == 2: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0,0.5,0.5,0])
    elif note % 12 == 4: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0,0.5,0,0.5])
    elif note % 12 == 5: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.5,0,0.5,0])
    elif note % 12 == 7: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0.5,0,0.5,0])
    elif note % 12 == 9: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0,0.5,0,0.5])
    elif note % 12 == 11: 
        change_note = np.random.choice(choice_list, 1, replace=False, p=[0,0.5,0,0.5])
    else:
        change_note = 0
    return int(change_note)


# 移除某些音
def remove_note(song):
    temp = copy.deepcopy(song)
    position = 1
#     while position % 2 != 0 and temp[position+1].time < delete_threshold:
    while position % 2 != 0 and temp[position].time <= 960 :
        position = random.randint(1,len(temp)-3)
    del temp[position]
    del temp[position]
    return temp


 # 增加裝飾音
def add_note(song, duration, num):
    temp = copy.deepcopy(song)
    for i in range(num):
        position = 1 # initial
        while position % 2 != 0 and position > len(temp)-2 and temp[position].time + temp[position+1].time != 240:
            position = random.randint(0,len(temp)-1)
        _note = temp[position].note
        interval = get_note(_note)
        if interval != 0 and temp[position].note == temp[position+1].note:
            temp.insert(position, (mido.Message('note_on', velocity = 101, note = _note + interval , time = 1)))
            temp.insert(position + 1, (mido.Message('note_on', velocity = 0, note = _note + interval, time = duration)))
            if  i+position+3 < len(temp)-1 and temp[i+position+3].time > duration+120:
                temp[i+position+3].time -= duration+1   # 下1個音時間要減短  
            elif  i+position+5 < len(temp)-1 and temp[i+position+5].time > duration+120:
                temp[i+position+5].time -= duration+1   # 下2個音時間要減短  
            elif i+position-3 < len(temp)-1 and temp[i+position-3].time > duration+120 :
                temp[i+position-3].time -= duration+1   # 前1個音時間要減短  
            elif i+position-5 < len(temp)-1 and temp[i+position-5].time > duration+120 :
                temp[i+position-5].time -= duration+1   # 前2個音時間要減短  
#             else:
#                 del temp[position]
#                 del temp[position]
#             else:
#                 temp = remove_note(temp)     
    return temp

# 新增一和音
def add_chord(song, num):
    temp = copy.deepcopy(song)
    for i in range(num):
        position = 1 # initial
        while position % 2 != 0:
            position = random.randint(0,len(temp)-1)
        _note = temp[position].note
        interval = get_chord(_note)
        if interval != 0 and position + 4 <= len(song) and temp[position].note == temp[position+1].note and temp[position+1].note != temp[position+2].note:
            temp.insert(position + 1, (mido.Message('note_on', velocity = 100, note = _note + interval , time = 0)))
            temp.insert(position + 3, (mido.Message('note_on', velocity = 0, note = _note + interval, time = 0)))
    return temp

