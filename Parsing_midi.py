#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mido
from mido import Message, MidiFile, MidiTrack
import copy
from collections import Counter
from music21 import *


# In[2]:


pitch_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def get_midi(filename, track=0):    
   ## read midi file
    mid = MidiFile(filename)
    ## get midi information
#     temp=[]
#     for msg in mid.tracks[track]:
#         temp.append(msg)
    temp = [msg for msg in mid.tracks[track]]
    ## only extract note_on and note_off
    midi_list = []
    for i in range(len(temp)):
#         if ('note_on' in str(temp[i]) or 'note_off' in str(temp[i])) and 'velocity=0' not in str(temp[i]):
        if ('note_on' in str(temp[i]) or 'note_off' in str(temp[i])):
            midi_list.append(temp[i])

    return midi_list


def get_pitch(num):
    return [pitch_list[num%12],int(num/12)]  #(pitch, octave)


def parse_midi(data):
    note_= []; velocity_= []; time_= []; midi_data=[]
    
    for i in range(len(data)-1):
        note_.append(get_pitch(data[i].note))
        velocity_.append(data[i].velocity)
        time_.append(data[i].time)
        midi_data.append((note_[i],velocity_[i], time_[i])) # merge all

    return midi_data

## seperate midi input into bars
def separate_song(song, threshold):
    a = song
    time = 0; t = []; t2 = []; n = []; n2 = []
    for i in range(len(a)):
        if i%2 == 0:
            time += a[i].time 
            time += a[i+1].time
            if time < threshold + 5:
                t.append(a[i])
                t.append(a[i+1])
                n.append(a[i].note%12)
                n.append(a[i+1].note%12)

            elif time > threshold + 10:
                t2.append(t)  # sepatate bar
                n2.append(n)  # index of note
                ## reset
                time = 0 
                time += a[i].time 
                time += a[i+1].time
                t = []
                n = []
                t.append(a[i])
                t.append(a[i+1])
                n.append(a[i].note%12)
                n.append(a[i+1].note%12)
         # 不滿threshold都補齊
        if i == len(a) - 2:
            t2.append(t)  # sepatate bar
            n2.append(n)  # index of note
    return n2, t2

