#!/usr/bin/python3

## @file
#
# turdus_m3rula_GUI.py
#
# GUI for turdus_m3rula SEP exploit
#
# Copyright (c) 2025-2026, ilikesn0w. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-only
#
##

import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import subprocess
import os
import re
import datetime

def run_a9x():
    try:
        a9x_name = "A9X.py"
        a9x_path = "./A9X.py"
        
        if not os.path.isfile(a9x_path):
            messagebox.showerror("Error", f"Executable file '{a9x_name}' not found in GUI dir")
            return
        
        os.chmod(a9x_path, 0o755)

        process = subprocess.Popen(["python3", a9x_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        root.quit()  
    except Exception as e:
        messagebox.showerror("Execution Error", f"Failed to run {a9x_name}: {str(e)}")

def run_a9x_t():
    try:
        a9x_t_name = "A9X_T.py"
        a9x_t_path = "./A9X_T.py"
        
        if not os.path.isfile(a9x_t_path):
            messagebox.showerror("Error", f"Executable file '{a9x_t_name}' not found in GUI dir")
            return
            
        os.chmod(a9x_t_path, 0o755)

        process = subprocess.Popen(["python3", a9x_t_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        root.quit()
    except Exception as e:
        messagebox.showerror("Execution Error", f"Failed to run {a9x_t_name}: {str(e)}")

def run_a10x():
    try:
        a10x_name = "A10X.py"
        a10x_path = "./A10X.py"
        
        if not os.path.isfile(a10x_path):
            messagebox.showerror("Error", f"Executable file '{a10x_name}' not found in GUI dir")
            return
            
        os.chmod(a10x_path, 0o755)

        process = subprocess.Popen(["python3", a10x_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        root.quit()
    except Exception as e:
        messagebox.showerror("Execution Error", f"Failed to run {a10x_name}: {str(e)}")

def run_a10x_t():
    try:
        a10x_t_name = "A10X_T.py"
        a10x_t_path = "./A10X_T.py"
        
        if not os.path.isfile(a10x_t_path):
            messagebox.showerror("Error", f"Executable file '{a10x_t_name}' not found in GUI dir")
            return
            
        os.chmod(a10x_t_path, 0o755)

        process = subprocess.Popen(["python3", a10x_t_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        root.quit()
    except Exception as e:
        messagebox.showerror("Execution Error", f"Failed to run {a10x_t_name}: {str(e)}")

root = tk.Tk()
root.title("Select your platform")

a9x_button = tk.Button(root, text="A9(X)", command=run_a9x)
a9x_button.pack(pady=10)

a9x_t_button = tk.Button(root, text="A9(X) Tethered", command=run_a9x_t)
a9x_t_button.pack(pady=10)

a10x_button = tk.Button(root, text="A10(X)", command=run_a10x)
a10x_button.pack(pady=10)

a10x_t_button = tk.Button(root, text="A10(X) Tethered", command=run_a10x_t)
a10x_t_button.pack(pady=10)

root.mainloop()
