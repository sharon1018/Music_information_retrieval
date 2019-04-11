#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import copy
import statistics
import numpy as np
import Parsing_midi as pm
import Init_chromo as init
import mido
import matplotlib.pyplot as plt
from mido import Message, MidiFile, MidiTrack
from collections import Counter


# 將note依照time拆成多個
def to_note_freq(midi_msg):     
    note_freq = []; count = 0
    for i in range(len(midi_msg)):
        if i % 2 == 0:
            for j in range(int((midi_msg[i].time + midi_msg[i+1].time)/240)):
                count += 1
                note_freq.append([midi_msg[i].note, count])
    return note_freq

# 計算面積差  
def count_area(ori_y, new_y):  
    area = 0
    for i in range(len(ori_y)):
        area += abs(ori_y[i]-new_y[i])
    return area

# smooth melody curve, sliding window = 7
def smooth(note_seq):  
    temp = []
    for i in range(len(note_seq)):
        if i < 4:
            temp.append(note_seq[i])
        elif i > len(note_seq) - 4:
            temp.append(note_seq[i])
        else:
            median = int(statistics.median(note_seq[i-4:i+4]))
            temp.append(median)
    return temp


# 校正頭尾
def correct_xy(xy1, xy2):
    if len(xy1) > len(xy2):
        xy1 = xy1[0:len(xy2)]
    else:
        xy2 = xy2[0:len(xy1)]
    return xy1, xy2

# melody matching
def count_area_score(ori_midi, new_midi, smooth_curve=True):  # smooth
    score = 0
    a = to_note_freq(ori_midi)
    b = to_note_freq(new_midi)
    a, b = correct_xy(a,b)
    # 拆成XY座標
    x = [i[1] for i in a]
    y = [i[0] for i in a]

    x2 = [i[1] for i in b]
    y2 = [i[0] for i in b]
    
    # smooth
    y_s1 = smooth(y)
    y_s2 = smooth(y2)

    if smooth_curve:
        area_diff = count_area(y_s1, y_s2)
#         print("smooth",area_diff)
        if area_diff > 0 and area_diff <= 90:
            score -= (area_diff / 10 * 2)
        if area_diff > 0 and area_diff <= 65:
            score += 15
        elif area_diff > 90:
            score -= 30 
    else:  
        area_diff = count_area(y, y2)
#         print("not smooth", area_diff)
        if area_diff > 0 and area_diff <= 70:
            score += (area_diff / 10 * 3)
            
#         elif area_diff > 60 and area_diff <= 70:
#             score += 10
#         elif area_diff > 50 and area_diff <= 60:
#             score += 8
        else:
            score += 0 
    return score

