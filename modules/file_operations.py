import re
import pandas as pd
import os
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from tkinter import messagebox


filetypes = (('Text Files', '*.txt'), ('Excel Files', '*.xlsx'))
root = tk.Tk()
root.withdraw()


def open_file():
    filepath = filedialog.askopenfilename(title="Select a data file..", filetypes=filetypes)

    if re.search(r'\.txt', filepath):
        #Open txt file
        data = []

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for f in file.readlines():
                    data.append(f.strip())
            
            messagebox.showinfo('Info', 'File open success')
            return data
        except:
            messagebox.showerror('Error','Open file error.')

    elif re.search(r'\.xlsx', filepath):
        # Open excel files
        try:
            df = dataframe_control(pd.read_excel(filepath))
            messagebox.showinfo('Info','File open success')
        except:
            messagebox.showerror('Error','Open file error.')
        return df
    else:
        return "null"

def save_file(data):
    filepath = filedialog.asksaveasfilename(title="Select a save file..", filetypes=filetypes)
    
    if re.search(r'\.txt', filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                for d in data:
                    file.write('\n')
                    file.write(d)
            messagebox.showinfo('Info', 'File save success')
        except:
            messagebox.showinfo('Error','File save error')
    elif re.search(r'\.xlsx', filepath):
        try:
            data.to_excel(filepath)
            messagebox.showinfo('Info','File save success')
        except:
            messagebox.showinfo('Error','File save error')

def file_control(path):
    try:
        os.path.exists(path)
        return True
    except:
        return False

def dataframe_control(df):
    
    try:
        control = df['ASIN NO']
        return df
    except:
        df = df.iloc[2::].rename(columns = {"Unnamed: 0": 'ASIN NO','Unnamed: 1': 'Kanada Price' })[:-1]
        return df