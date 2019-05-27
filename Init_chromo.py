## Initialize - Generate chromosome

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


def note_series(interval, _note, duration):
    m = []
    for i in range(len(interval)):
        m.append(mido.Message('note_on', velocity = 105, note = _note + interval[i], time = 1))
        m.append(mido.Message('note_on', velocity = 0, note = _note + interval[i], time = duration - 1))
    return m
  
melody_series = [[0,-5,0,4],[0,0,0,0], [0,-8,-3,0],[0,0,0,0],[0,-9,-4,0],[0,-8,-3,0],[0,0,0,0], [0,-7,-3,0],[0,0,0,0], [0,-7,-4,0],[0,0,0,0],[0,-9,-4,0]]
melody_series2 = [[0,-1,0,2],[0,0,0,0], [0,-5,-3,0],[0,0,0,0],[0,-4,-2,0],[0,-1,-3,0],[0,0,0,0], [0,-7,-5,0],[0,0,0,0], [0,-2,0,2],[0,0,0,0],[0,-2,-4,0]]
melody_list = [melody_series, melody_series2]

def add_melody(song):
    position = 2
    temp = copy.deepcopy(song)
    # 將長度為四分音符的分解為4個16分音符
    while temp[position].time + temp[position+1].time < 240:
        position = random.randrange(2,len(temp)-2, 2)  
    _note = temp[position].note
    idx = _note % 12 
    t = temp[position].time + temp[position+1].time
    
    # 移除選中的四分音符
    del temp[position]
    del temp[position]
    
    # 替換成4個16分音符
    interval = melody_series[idx]
    m = note_series(interval, _note, int(t/4))
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
def remove_note(song, duration):
    temp = copy.deepcopy(song)
    position = 1
    while position % 2 != 0 and temp[position].time < duration :
        position = random.randint(0,len(temp)-3)
    del temp[position]
    del temp[position]
    return temp

 # 延長長度過短的音 (unused)
def change_duration(song, threshold, duration): # one beat = 480
    i = 0   
    temp = copy.deepcopy(song)
    while i % 2 != 0 :
        i = random.randrange(2,len(temp)-4, 2)     
    while temp[i].velocity != 0 and temp[i].time + temp[i+1].time <= threshold:
        temp[i+1].time = temp[i+1].time + duration
        temp[i+3].time = temp[i+3].time - duration
    return temp

def add_note(song):
    temp = copy.deepcopy(song)
    position = 0
    while temp[position].time + temp[position+1].time < 480:
        position = random.randrange(2,len(temp)-2, 2)
    _note = temp[position].note
    idx = _note % 12 
    # 移除選中的四分音符
    del temp[position]
    del temp[position]
    
    _note = get_note(temp[position].note)
    
#     # add note
    m = []
    m.append(mido.Message('note_on', velocity = 105, note = _note + temp[position].note, time = 1))
    m.append(mido.Message('note_on', velocity = 0, note = _note + temp[position].note, time = 119))
    temp[position:position] = m  
    return temp

