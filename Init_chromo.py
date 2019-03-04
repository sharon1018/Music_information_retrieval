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
   
    
 # 增加裝飾音
def add_note(song, interval, duration):
    position = 1
    while position % 2 != 0:
        position = random.randint(0,len(song)-1)
    _note = song[position].note
    song.insert(position, (mido.Message('note_on', note = _note + interval , time = 1)))
    song.insert(position + 1, (mido.Message('note_on', note = _note + interval, time = duration)))
    return song

# 移除某些音
def remove_note(song, delete_threshold):
    position = 1
    while position % 2 != 0 and song[position+1].time < delete_threshold:
        position = random.randint(0,len(song)-1)
    del song[position]
    del song[position]
    return song