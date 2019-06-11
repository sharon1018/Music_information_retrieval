import count_CE as ce

C_pitch = [0, -1, 2, -1, 4, 5, -1, 7, -1, 9, -1, 11]  # there is no sharp and flat in C scale, so set it as -1
chord_list = [[0,4,7],[-1,-1,-1],[2,5,9],[-1,-1,-1],[4,7,11],[5,9,0],[-1,-1,-1],[7,11,2],[-1,-1,-1],[9,0,4],[-1,-1,-1],[11,2,5]]
pitch_list = ['C','D','E','F','G','A','B']
scale_list = [0,2,4,5,7,9,11]  # = midi notes = ['C','D','E','F','G','A','B']    
harmony = [[0,2,4,7,-3,-5,-1], [0], [0,5,-2,-3,-7,2,3],[0], [0,3,1,-4,-2,-7], [0,2,4,5,7,-1,-3,-6],\
[0], [0,2,4,5,7,-2,-3,-5,-7], [0],[0,2,3,7,-2,-7,-5],[0],[1,3,0,-4,-2,-9]]
surprise_list = [1,3,6,8,10]

def ce_score(CE, CE_):
    score_ce = 0  
    dist = ce.count_distance(CE, CE_)   
    if dist == 0.0:  # the chord remain
        score_ce = 100
    elif dist > 0 and dist <= 2:
        score_ce = 100-5*(dist)
    elif dist > 2 and dist <= 4:
        score_ce = 100-7*(dist)
    elif dist > 4 :
        score_ce = 100-9*(dist)
    else:
        print("NONE")
    return score_ce

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

    # score every notes based on harmony rule (40%)
    for i in range(len(midi_msg)):  # TODO: if len==1
        if i % 2 == 0:
            d = (midi_msg[i].time + midi_msg[i+1].time) / 480
            
            if midi_msg[i].note in ori_note: # keep original melody
                score_harmony += (5 * d)

            elif midi_msg[i].note not in ori_note:
                score_harmony -= (5 * d) 
            
            if midi_msg[i].note % 12 == chord[0]:  # if the note is chord root note
                score_harmony += (5 * d)
            if midi_msg[i].note % 12 == chord[1]:  # if the note is 2nd note
                score_harmony += (5 * d)
            if midi_msg[i].note % 12 == chord[2]:  # if the note is 3rd note
                score_harmony += (5 * d)
                
            if midi_msg[i].note % 12 not in chord: # note is not a chord note
                score_harmony -= (5 * d)  
            
            if midi_msg[i].note % 12 not in scale_list:  # note not in the scale (C major)
                score_harmony -= (5 * d) 
            
            if midi_msg[i].note % 12 in scale_list:  # note in the scale (C major)
                score_harmony += (5 * d)  
                
            if i < len(midi_msg) - 3 and abs(midi_msg[i].note - midi_msg[i+2].note) > 9:  # big jump notes
                score_harmony -= (5 * abs(midi_msg[i].note - midi_msg[i+2].note) * d)        

            if i < len(midi_msg) - 3 and abs(midi_msg[i].note - midi_msg[i+2].note) == 12:  # 8 d egree
                score_harmony += (5 * d) 
                

            ## 每個音和諧的degree
            harmony_list = harmony[midi_msg[i].note % 12]
            if i < len(midi_msg) - 3 and midi_msg[i+2].note - midi_msg[i].note in harmony_list:
                score_harmony += (5 * d)        
            if i < len(midi_msg) - 3 and midi_msg[i+2].note - midi_msg[i].note not in harmony_list:
                score_harmony -= (5 * d)

            # duration
            if d < 2: 
                score_harmony += 5  
            if d > 2: 
                score_harmony -= 5    
                    
    return score_harmony