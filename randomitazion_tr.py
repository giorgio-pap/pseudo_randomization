#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:10:44 2020

@author: papitto
"""
import pandas as pd
from zipfile import ZipFile

#if using PY3 change raw_input to input

group_info = raw_input("What is the subject GROUP?") 
type(group_info)


subj_info = raw_input("What is the subject NUMBER?") 
type(subj_info)

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


for iterations in range(0,12):
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
            except KeyError:
                pass
    

    class ReplaceWithNext:
        def __init__(self, **kwargs):
            self.lookup = {k: iter(v) for k, v in kwargs.items()}
        def __call__(self, value):
            return next(self.lookup[value])
    
    for i, row in experimental_df_2.iterrows():
        experimental_df_2.at[i, 'img_fix_1'] = "cues/fix_1.png"
        experimental_df_2.at[i, 'img_fix_2'] = "cues/fix_2.png"
    
    #export the excel file
    experimental_df_2.to_excel("participants_trials/" +'Group' + group_info + n_dataset + "_" + subj_info + '.xlsx', index=False) #creates a new excel from the concatenated dataframe                                       
    
# create a ZipFile object
zipObj = ZipFile("participants_trials/" + "trials_" + group_info + "_" + subj_info + ".zip", 'w')
zip_int = 0

# Add multiple files to the zip
for iterations_2 in range(0,12):
    zip_int += 1
    zip_str = str(zip_int)
    zipObj.write("participants_trials/" + 'Group' + group_info + zip_str + "_" + subj_info + '.xlsx')

# close the Zip File
zipObj.close()
