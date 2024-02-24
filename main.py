#This is a program that will take in multiple directories and read the trial contents from vicon to determine which ones have been cropped or not

import os
import tkinter as tk
from tkinter import filedialog
import c3d
import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_rowcol_to_cell

zero_frame_trials = []
cropped_trials = []
data = []
dirs = []
dir_filename = {}

#function used later to get the first frame of a trial 
def get_trial_start_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():
            if i == 1:
                return points
            
#functions to get subdirectories from main directory
def list_subdirectories(parent_directory):
    subdirectories = [subdir for subdir in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, subdir))]
    return subdirectories

#ask for the parent directory
parent_directory = filedialog.askdirectory(title="Select directories containing trial files")

dirs = list_subdirectories(parent_directory)
            
#create root window
root = tk.Tk()
root.withdraw() #Hides root window



#Ask the user to select multiple directories and store them in dirs
#while True:
    #sets directories equal to selection
#    directories = filedialog.askdirectory(title="Select directories containing trial files")

    #If statement that determines if you hit cancel or selected a directory
#    if directories != '':
#        dirs.append(directories)
#        if not directories:
#            break
#    else:
#        break





    

print (dirs)

#Main loop to iterate through each file
if dirs:
    for directory in dirs:
        
        #Lists to store trials starting at 0 frames and trials starting at >0 frames
        

        #Now that we'er in a directory go through each file 
        for filename in os.listdir(directory):
            #find the files that end with .c3d
            if filename.endswith(".c3d"):
                file_path = os.path.join(directory, filename)

                #run our file through get trial start frame
                start_frame = get_trial_start_frame(file_path)

                #test
                print(start_frame)

                #deciding which list to put the file in


                if start_frame is None:
                    cropped_trials.append(filename)
                    data.append({'Directory': directory, 'Trials starting after 0 frames': ''.join(filename)})
                else:
                    zero_frame_trials.append(filename)
                    data.append({'Directory': directory, 'Trials starting at 0 frames': ''.join(filename)})
            

    #DataFrame from data
    df = pd.DataFrame(data)

    #Ask the user to specify name and file location for excel file
    excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])

    #Write DataFram to excel

    print(excel_file_path)

    if excel_file_path:
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']


        

        
        writer.close()
        print("Excel Saved Success")
    else:
        print("No File selected")
    
    

    




                


else:
    print("No directories selected.")

print (f'{zero_frame_trials}{cropped_trials}')