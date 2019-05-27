C_pitch = [0, -1, 2, -1, 4, 5, -1, 7, -1, 9, -1, 11]  # there is no sharp and flat in C scale, so set it as -1
chord_list = [[0,4,7],[-1,-1,-1],[2,5,9],[-1,-1,-1],[4,7,11],[5,9,0],[-1,-1,-1],[7,11,2],[-1,-1,-1],[9,0,4],[-1,-1,-1],[11,2,5]]
pitch_list = ['C','D','E','F','G','A','B']
scale_list = [0,2,4,5,7,9,11]  # = midi notes = ['C','D','E','F','G','A','B']    
harmony = [[0,2,4,7,-3,-5,-1], [0], [0,5,-2,-3,-7,2,3],[0], [0,3,1,-4,-2,-7], [0,2,4,-1,-3,-6],\
[0], [0,2,4,7,-2,-3,-5], [0],[0,2,3,7,-2,-7,-5],[0],[1,3,0,-4,-2,-9]]

# invalid = [[],[0],[],[0],[],[],[0],[],[0],[],[0],[]] # TODO

def harmony_score(midi_msg, chord, ori_note): 
    score_harmony = 0
    ## get chord note, ie: C major is CEG
    c = int(list(chord)[2])
    if c % 12 in C_pitch:
        chord = chord_list[c % 12]
    elif (c + 1) % 12 in C_pitch:
        chord = chord_list[(c + 1) % 12]
    elif (c - 1) % 12 in C_pitch:
        chord = chord_list[(c - 1) % 12]

    ## score every notes based on harmony rule (40%)
    for i in range(len(midi_msg)):  # TODO: if len==1
        if i % 2 == 0:
            d = (midi_msg[i].time + midi_msg[i+1].time)/480
            
            if midi_msg[i].note in ori_note: # keep original melody
                score_harmony += (4 * d)
#                 print("note in ori_note", score_harmony)
            elif midi_msg[i].note not in ori_note:
                score_harmony -= (2 * d) 
#                 print("note not in ori_note", score_harmony)
            
            if midi_msg[i].note % 12 == chord[0]:  # if the note is chord root note
                score_harmony += (6 * d)
#                 print("note in chord 1 note", score_harmony)
            elif midi_msg[i].note % 12 == chord[1]:  # if the note is 2nd note
                score_harmony += (4 * d)
#                 print("note in chord 2 note", score_harmony)
            elif midi_msg[i].note % 12 == chord[2]:  # if the note is 3rd note
                score_harmony += (4 * d)
#                 print("note in chord 3 note", score_harmony)
                
            if i == 0 and midi_msg[i].note % 12 == chord[0]:  # the note is the first note and is a chord root note
                score_harmony += 6
#                 print("1 note and note in chord 1 note", score_harmony)
            elif i == 0 and midi_msg[i].note % 12 == chord[1]:  # the note is the first note and is a 2nd chord note
                score_harmony += 4
#                 print("1 note and note in chord 2 note", score_harmony)
            elif i == 0 and midi_msg[i].note % 12 == chord[2]:  # the note is the first note and is a 3rd chord note
                score_harmony += 4      
#                 print("1 note and note in chord 3 note", score_harmony)
                
            if i == len(midi_msg)-2 and midi_msg[i].note % 12 == chord[0]: # the note is the last note and is a chord root note
                score_harmony += 6
#                 print("-1 note and note in chord 1 note", score_harmony)
            elif i == len(midi_msg)-2 and midi_msg[i].note % 12 == chord[1]: # the note is the last note and is a 2nd chord note
                score_harmony += 4
#                 print("-1 note and note in chord 2 note", score_harmony)
            elif i == len(midi_msg)-2 and midi_msg[i].note % 12 == chord[2]: # the note is the last note and is a 3rd chord note
                score_harmony += 4      
#                 print("-1 note and note in chord 3 note", score_harmony)
                
            if i == 0 and midi_msg[i].note % 12 not in chord: # not in chord note
                score_harmony -= (3 * d) 
#                 print("1 note and note not in chord", score_harmony)
            if i == len(midi_msg)-2 and midi_msg[i].note % 12 not in chord: # not in chord note
                score_harmony -= (3 * d)  
#                 print("-1 note and note not in chord", score_harmony)
                
            if midi_msg[i].note % 12 not in chord: # note is not a chord note
                score_harmony -= (5 * d)  
#                 print("note not in chord", score_harmony)
            if midi_msg[i].note % 12 not in scale_list:  # note not in the scale (C major)
                score_harmony -= (10 * d) 
#                 print("midi_note", midi_msg[i].note, "note not in scale", score_harmony)
            elif midi_msg[i].note % 12 in scale_list:  # note in the scale (C major)
                score_harmony += (2 * d)  
#                 print("in scale", score_harmony)
                
            if i < len(midi_msg) - 3 and abs(midi_msg[i].note - midi_msg[i+2].note) >= 7:  # big jump notes
                score_harmony -= (2 * abs(midi_msg[i].note - midi_msg[i+2].note) * d)  
#                 print("big jump", score_harmony)
            if i < len(midi_msg) - 3 and abs(midi_msg[i].note - midi_msg[i+2].note) == 0:  # repetitive notes
                score_harmony -= 4  
#                 print("repetitive", score_harmony)
                
            ## 每個音和諧的degree
            harmony_list = harmony[midi_msg[i].note % 12]
            if i < len(midi_msg) - 3 and midi_msg[i+2].note - midi_msg[i].note in harmony_list:
                score_harmony += (8 * d)  
#                 print("note in harmony list", score_harmony)
            if i < len(midi_msg) - 3 and midi_msg[i+2].note - midi_msg[i].note not in harmony_list:
                score_harmony -= (8 * d)
#                 print("note not in harmony list", score_harmony)

            # duration
            if d > 0.4 and d < 2: 
                score_harmony += 6    
#                 print("duration", score_harmony)
            elif d < 0.25: # the duration of the note is too short
                score_harmony -= 6 
#                 print("short duration", score_harmony)
    
    score_harmony /= (len(midi_msg)/2)
#     print("--------final {}----------".format(score_harmony))
        
    return score_harmony