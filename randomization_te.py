#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:16:25 2020

@author: andrea
"""

import pandas as pd
from zipfile import ZipFile
import shutil, os
import numpy as np
from random import shuffle

#if using PY2 change input to raw_input

randomized = False

while not randomized:
    value_1 = 0
    value_2 = 0
    
    x1=[2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6] # possible duration of a jitter
    x1 = np.repeat(x1,26)
    x2=[2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6] # possible duration of a jitter
    x2= np.repeat(x2,26)
    
    shuffle(x1)
    shuffle(x2)
    
    #x_r_1 = random.sample(x1, 228) # fixation cross
    #x_r_2 = random.sample(x1, 228) # inter cue interval (ICI)

    x_r_1 = x1[0:228]
    x_r_2 = x2[0:228]
    
    df_1 = pd.DataFrame({'Freq_1': x_r_1})
    df_2 = pd.DataFrame({'Freq_2': x_r_2}) # ICI
    
    merged_jitters = pd.concat([df_1, df_2], axis=1) #make a new dataframe 
            
    jitters_fix = merged_jitters['Freq_1']
    jitters_ICI = merged_jitters['Freq_2']
        
    x_r_1 = jitters_fix.tolist()
    x_r_2 = jitters_ICI.tolist()
        
    chunk_fill_spec = x_r_1[0:12]
    chunk_fill_sub = x_r_1[12:24]
    chunk_fill_rule = x_r_1[24:36]
    chunk_spec = x_r_1[36:84]
    chunk_sub = x_r_1[84:132]
    chunk_rule = x_r_1[132:180]
    chunk_gen = x_r_1[180:228]
    
    
    if (sum(chunk_rule) and sum(chunk_spec) and sum(chunk_sub) and sum(chunk_gen) > 180) and (sum(chunk_rule) and sum(chunk_spec) and sum(chunk_sub) and sum(chunk_gen) < 200):
        print("ok_1")
        value_1 = 1
    elif (sum(chunk_rule) or sum(chunk_spec) or sum(chunk_sub) or sum(chunk_gen) <= 180) or (sum(chunk_rule) or sum(chunk_spec) or sum(chunk_sub) or sum(chunk_gen) >= 200):
        print("no")
        value_1 = 0


    chunk_fill_spec_2 = x_r_2[0:12]
    chunk_fill_sub_2 = x_r_2[12:24]
    chunk_fill_rule_2 = x_r_2[24:36]
    chunk_spec_2 = x_r_2[36:84]
    chunk_sub_2 = x_r_2[84:132]
    chunk_rule_2 = x_r_2[132:180]
    chunk_gen_2 = x_r_2[180:228]        
    
    if (sum(chunk_rule_2) and sum(chunk_spec_2) and sum(chunk_sub_2) and sum(chunk_gen_2) > 180) and (sum(chunk_rule_2) and sum(chunk_spec_2) and sum(chunk_sub_2) and sum(chunk_gen_2) < 200):
        print("ok_2")
        value_2 = 1
    elif (sum(chunk_rule_2) or sum(chunk_spec_2) or sum(chunk_sub_2) or sum(chunk_gen_2) <= 180) or (sum(chunk_rule_2) or sum(chunk_spec_2) or sum(chunk_sub_2) or sum(chunk_gen_2) >= 200):
        print("no_2")
        value_2 = 0
    
    
    if (value_1 + value_2) > 1:
        randomized=True
    else:
        print("no_sum")
        
# participant information - type in
group_info = input("What is the subject GROUP?") 
type(group_info)


subj_info = input("What is the subject NUMBER?") 
type(subj_info)


#this script concatenates 6 files of 38 trials each mantaining the same criteria within and across files
looping = 0


while (looping == 0):
    n_dataset_int = 0
    n_dataset = str(n_dataset_int)
    
    #open the file with experimental and filler trials
    df_all_possible_trials = pd.read_excel('Group' + group_info + n_dataset + '.xlsx')
    
    #extract filler trials
         
    df_filler_rule = df_all_possible_trials.loc[df_all_possible_trials['conditions'] == "fill_rule"]
    df_filler_sub_rule = df_all_possible_trials.loc[df_all_possible_trials['conditions'] == "fill_sub_rule"]
    df_filler_spec = df_all_possible_trials.loc[df_all_possible_trials['conditions'] == "fill_spec"]
    
    #extract the experimental trials - all of them
    df_experimental = df_all_possible_trials.loc[df_all_possible_trials['trial_type'] == "experimental"]
    
    
    for iterations in range(0,13):
        #sample two filler trials per condition 
        df_filler_rule_1 = df_filler_rule.sample(n=2)     
        df_filler_sub_rule_1 = df_filler_sub_rule.sample(n=2)
        df_filler_spec_1 = df_filler_spec.sample(n=2) #6 = ca 15% of 38 
    
        # concat all the dataframes
        frames = [df_filler_rule_1, df_filler_sub_rule_1, df_filler_spec_1, df_experimental]
        df_experiment_concat = pd.concat(frames, ignore_index=True)
        
        df_experiment = df_experiment_concat.sample(n=38)
        df_experiment.reset_index(drop=True, inplace=True)
        
        #max color1expl cannot be identical in 3 consecutive trials
        #max color2expl cannot be identical in 3 consecutive trials
        #trials cannot be filler in 2 consecutive trials
        n_dataset_int += 1
        n_dataset = str(n_dataset_int)
        
        #randomize
        randomized = False
        
        while not randomized:
            experimental_df_2 = df_experiment.sample(frac=1).reset_index(drop=True) # where experimental_df_2 is the original file read in
            for i in range(0, len(experimental_df_2)):
                try:
                    if i == len(experimental_df_2) - 1:
                        randomized = True
                    elif (experimental_df_2['numbers_pr'][i] != experimental_df_2['numbers_pr'][i+1]) and ((experimental_df_2['color1expl'][i] != experimental_df_2['color1expl'][i+1]) and (experimental_df_2['color1expl'][i] != experimental_df_2['color1expl'][i+2])) and ((experimental_df_2['color2expl'][i] != experimental_df_2['color2expl'][i+1]) and (experimental_df_2['color2expl'][i] != experimental_df_2['color2expl'][i+2])):
                        continue
                    elif (experimental_df_2['numbers_pr'][i] == experimental_df_2['numbers_pr'][i+1]) or ((experimental_df_2['color1expl'][i] == experimental_df_2['color1expl'][i+1]) and (experimental_df_2['color1expl'][i] == experimental_df_2['color1expl'][i+2])) or ((experimental_df_2['color2expl'][i] == experimental_df_2['color2expl'][i+1]) and (experimental_df_2['color2expl'][i] == experimental_df_2['color2expl'][i+2])):
                        break    
                except: #IndexError:
                    pass

        #export the excel file
        experimental_df_2["file_number"] = n_dataset #file_n matches the number of the excel file created
        experimental_df_2.to_excel("Group" + group_info +  "_r" + n_dataset + '.xlsx', index=False) #creates a new excel from the concatenated dataframe                                       
    
    df_0 = pd.read_excel("Group" + group_info + "_r1.xlsx")
    df_0.to_excel("Group" + group_info + "_total.xlsx", index=False) # this creates a copy of file #1 so that the 1st file will not be modified, instead values are going to be added to the "total" file
    
    n_dataset_int = 0
    n_dataset = str(n_dataset_int)
    
    x = 37 #number rows
    y = 38*6 
    
    for iterations in range(0,6):
        n_dataset_int +=1
        n_dataset = str(n_dataset_int)
        n_dataset_plus_int = n_dataset_int+1
        n_dataset_plus = str(n_dataset_plus_int)
    
        
        df_1 = pd.read_excel("Group" + group_info + "_total.xlsx") #at the first iteration, this is equal to file n.1
        df_2 = pd.read_excel("Group" + group_info + "_r" + n_dataset_plus + '.xlsx') #at the first iteration, this is equal to file n.2 
        print(n_dataset)
    
        if (df_1['numbers_pr'][x] != df_2['numbers_pr'][0]) and ((df_1['color1expl'][x] != df_2['color1expl'][0]) and (df_1['color1expl'][x] != df_2['color1expl'][1])) and ((df_1['color2expl'][x] != df_2['color2expl'][0]) and (df_1['color2expl'][x] != df_2['color2expl'][1])):
            df_1_2 = [df_1, df_2]
            df_1_2 = pd.concat(df_1_2, ignore_index=True)
            df_1_2.to_excel("Group" + group_info + "_total.xlsx", index=False) #creates a new excel from the concatenated dataframe                                                  
            x = x+38 
        elif (df_1['numbers_pr'][x] == df_2['numbers_pr'][0]) or ((df_1['color1expl'][x] == df_2['color1expl'][0]) and (df_1['color1expl'][x] == df_2['color1expl'][1])) or ((df_1['color2expl'][x] == df_2['color2expl'][0]) and (df_1['color2expl'][x] == df_2['color2expl'][1])):
            break    
       
      
    if x >= y: #if there are at least 228 rows in the "total" file, stop and get the first rows
        fObj1 = df_1_2.head(228) 
        looping = 1 
        print("done")
    else:
        print("restart")
        continue  

class ReplaceWithNext:
    def __init__(self, **kwargs):
        self.lookup = {k: iter(v) for k, v in kwargs.items()}
    def __call__(self, value):
        return next(self.lookup[value])
    

fObj1['Jitter_Fix'] = fObj1['conditions'].apply(ReplaceWithNext(spec=chunk_spec, subrule=chunk_sub, rule=chunk_rule, general=chunk_gen, 
     fill_spec=chunk_fill_spec, fill_sub_rule=chunk_fill_sub, fill_rule=chunk_fill_rule))
fObj1['Jitter_ICI'] = fObj1['conditions'].apply(ReplaceWithNext(spec=chunk_spec_2, subrule=chunk_sub_2, rule=chunk_rule_2, general=chunk_gen_2, 
     fill_spec=chunk_fill_spec_2, fill_sub_rule=chunk_fill_sub_2, fill_rule=chunk_fill_rule_2))

for i, row in fObj1.iterrows():
    fObj1.at[i, 'img_fix_1'] = "cues/fix_1.png"
    fObj1.at[i, 'img_fix_2'] = "cues/fix_2.png"

#######
file_n = [1]*38 + [2]*38 + [3]*38 + [4]*38 + [5]*38 + [6]*38
####
    
fObj1.to_excel("Group" + group_info + "_" + subj_info + "_total.xlsx", index=False) #creates a new excel from the concatenated dataframe

 # create a ZipFile object
zipObj = ZipFile("Group" + group_info + "_" + subj_info + ".zip", 'w')
zip_int = 0

# Add multiple files to the zip
for iterations_2 in range(0,13):
    zip_int += 1
    zip_str = str(zip_int)
    zipObj.write("Group" + group_info + "_r" + zip_str + '.xlsx')
zipObj.write("Group" + group_info + "_" + subj_info + "_total.xlsx")
zipObj.write("Group" + group_info + "_total.xlsx")

# close the Zip File
zipObj.close() 

#move it into data folder
shutil.move("Group" + group_info + "_" + subj_info + ".zip", "Group" + group_info + "_" + subj_info + ".zip")    
shutil.move("Group" + group_info + "_" + subj_info + "_total.xlsx", "resources/Group" + group_info + "_" + subj_info + "_total.xlsx")    

file_int = 0
for iterations_3 in range(0,13):
    file_int += 1
    file_str = str(file_int)
    os.remove("Group" + group_info + "_r" + file_str + '.xlsx')
os.remove("Group" + group_info + "_total.xlsx")  
