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
    temp=[]
    for msg in mid.tracks[track]:
        temp.append(msg)
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

def separate_phrase(base, midi_list, threshold):
    start = midi_list[0].time % 1920
    midi_list[0].time = start + base

    count = 0; mid = []; temp = []
    for i in range(len(midi_list)):
        count += midi_list[i].time
        if count <= threshold:  
            temp.append(midi_list[i])
        else:
            temp.append(midi_list[i])
            mid.append(temp)
            count = 0
            temp = [] 
    return mid

