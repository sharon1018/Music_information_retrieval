#!/usr/bin/env python
# coding: utf-8

# In[1]:
import librosa
import os, sys
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks
import warnings
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import itertools
from librosa import display
warnings.filterwarnings('ignore')
import mido
from mido import Message, MidiFile, MidiTrack


# In[2]:


# pitch_ary = [[1,0,1], [0,1,8], [-1,0,3], [0,-1,10], [1,0,5], [0,1,0], [-1,0,7],\
#                  [0,-1,2], [1,0,9], [0,1,4], [-1,0,11], [0,-1,6]]

pitch_ary = [[0,1,0], [-1,0,7], [0,-1,2], [1,0,9], [0,1,4], [-1,0,11], [0,-1,6], [1,0,1], [0,1,8], [-1,0,3], [0,-1,10], [1,0,5]]

pitch_ary = np.array(pitch_ary)


## get all clip 
def get_dirs(path):
    dirs = os.listdir(path)
    return dirs  # file list

## use the list's index to get the corresponding pitch
def pitch_trans(seq):
    pitch_list = ['C','C#','D','D#(E-)','E','F','F#','G','G#','A','A#(B-)','B']
    return pitch_list[seq]

## transform pitch to array in space
def pitch_to_ary(notes):
#     pitch_ary = [[1,0,1], [0,1,8], [-1,0,3], [0,-1,10], [1,0,5], [0,1,0], [-1,0,7],\
#                  [0,-1,2], [1,0,9], [0,1,4], [-1,0,11], [0,-1,6]]
    
    pitch_ary = [[0,1,0], [-1,0,7], [0,-1,2], [1,0,9], [0,1,4], [-1,0,11], [0,-1,6], [1,0,1], [0,1,8], [-1,0,3], [0,-1,10], [1,0,5]]
    
    pitch_ary = np.array(pitch_ary)
    return pitch_ary[notes]


## count CE
def count_CE(notes_seq):
    c = Counter(notes_seq)
    Dab = 0
    sum_dp = 0
    for i in range(len(notes_seq)):
        pij = (pitch_to_ary(notes_seq[i]))
        dij = 1
        Dab = sum(c.values())
        sum_dp += (dij * pij)  
        CE = sum_dp/Dab   
    return CE

def get_key(CE, pitch_ary):
    key = []
    for i in range(len(pitch_ary)):
        key.append(abs(pitch_ary[i][0]-int(CE[0])) + abs(pitch_ary[i][1]-int(CE[1])) + abs(pitch_ary[i][2]-int(CE[2])))
    predict_key = pitch_trans(key.index(min(key)))
    return predict_key


def get_key_list(file):
    key_ = []; result = []
    for i in range(len(file)):
        CE = count_CE(file[i])
        key_.append(get_key(CE, pitch_ary))
    return key_

# def get_key(CE, pitch_ary):
#     sa1=[];sa2=[];sa3=[];key=[];key_idx=[]
#     for i in range(len(pitch_ary)):
#         sa1.append(abs(pitch_ary[i][0]-int(CE[0])) + abs(pitch_ary[i][1]-int(CE[1])) + abs(pitch_ary[i][2]-int(CE[2])))
#         sa2.append(abs(pitch_ary[i][0]-int(CE[0])) + abs(pitch_ary[i][1]-int(CE[1])) + abs(pitch_ary[i][2]-12-int(CE[2])))
#         sa3.append(abs(pitch_ary[i][0]-int(CE[0])) + abs(pitch_ary[i][1]-int(CE[1])) + abs(pitch_ary[i][2]+12-int(CE[2])))
#     key.append((min(sa1), min(sa2), min(sa3))) # save value
#     key_idx.append((sa1.index(min(sa1)), sa2.index(min(sa2)), sa3.index(min(sa3)))) # save index
#     min_idx = key.index(min(key))
#     predict_key = pitch_trans(key_idx[0][min_idx])
#     return predict_key



