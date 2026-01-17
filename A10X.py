#!/usr/bin/python3

## @file
#
# A10X.py
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

def process_log_line(line):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_pattern = re.compile(r"- \x1b\[36m<Log> \x1b\[39m\x1b\[32m")
    return log_pattern.sub(f"[{current_time}]", line)

def select_ipsw():
    global IPSW
    IPSW = filedialog.askopenfilename(title="Select IPSW file", filetypes=[("IPSW files", "*.ipsw")])
    if IPSW:
        messagebox.showinfo("File Selected", f"You selected: {IPSW}")
    else:
        messagebox.showwarning("Error", "You didn't select an IPSW file")

def select_shsh2():
    global SHSH2
    SHSH2 = filedialog.askopenfilename(title="Select SHSH2 file", filetypes=[("SHSH2 files", "*.shsh2")])
    if SHSH2:
        messagebox.showinfo("File Selected", f"You selected: {SHSH2}")
    else:
        messagebox.showwarning("Error", "You didn't select a SHSH2 file")

def fix_permissions():
    try:
        program_name = "xattr"
        program_path = "/usr/bin/xattr"

        if not os.path.isfile(program_path):
            messagebox.showerror("Error", f"Executable file '{program_name}' not found in /usr/bin")
            return

        files = ["./bin/turdusra1n", "./bin/turdus_merula", "./bin/lib/libirecv.dylib"]
        for file in files:
            if os.path.isfile(file):
                subprocess.run([program_path, "-c", file], check=True)
        
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Permissions fixed successfully.\n")
        output_text.see(tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
def run_turdusra1n():
    try:
        program_name = "turdusra1n"
        program_path = "./bin/turdusra1n"

        if not os.path.isfile(program_path):
            messagebox.showerror("Error", f"Executable file '{program_name}' not found in ./bin")
            return

        process = subprocess.Popen([program_path, "-ED"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
def get_nonce_from_shsh2():
    global nonce
    if not SHSH2:
        messagebox.showerror("Error", "Please select a SHSH2 file first.")
        return

    try:
        with open(SHSH2, "r", encoding="utf-8") as file:
            content = file.read()

        match = re.search(r"<key>generator</key>\s*<string>(0x[0-9A-Fa-f]+)</string>", content)
        if match:
            nonce = match.group(1)
            messagebox.showinfo("Nonce Extracted", f"Nonce: {nonce}")
        else:
            messagebox.showerror("Error", "Could not extract nonce from SHSH2 file.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading SHSH2 file: {e}")

def run_turdusra1n_nonce():
    if not nonce:
        messagebox.showerror("Error", "Nonce is not set. Please extract it from SHSH2 first.")
        return

    try:
        program_name = "turdusra1n"
        program_path = "./bin/turdusra1n"

        if not os.path.isfile(program_path):
            messagebox.showerror("Error", f"Executable file '{program_name}' not found in ./bin")
            return

        process = subprocess.Popen([program_path, "-EDb", nonce], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def restore_turdus_merula_ipsw():
    try:
        if not SHSH2 or not IPSW:
            messagebox.showerror("Error", "Please select both a SHSH2 and an IPSW file.")
            return

        merula_name = "turdus_merula"
        merula_path = "./bin/turdus_merula"

        if not os.path.isfile(merula_path):
            messagebox.showerror("Error", f"Executable file '{merula_name}' not found in ./bin")
            return

        process = subprocess.Popen([merula_path, "-w", "--load-shsh", SHSH2, IPSW],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Turdus Merula GUI (A10(X) Untethered)")

logo = tk.PhotoImage(file="./resources/png/Logo400x400.png")
logo_label = tk.Label(root, image=logo)
logo_label.place(x=135, y=0)

perm_button = tk.Button(root, text="Fix permissions", command=fix_permissions)
perm_button.pack(pady=10)

select_shsh2_button = tk.Button(root, text="Select SHSH2", command=select_shsh2)
select_shsh2_button.pack(pady=10)

get_and_set_nonce_button = tk.Button(root, text="Get and set nonce", command=get_nonce_from_shsh2)
get_and_set_nonce_button.pack(pady=10)

select_ipsw_button = tk.Button(root, text="Select IPSW file", command=select_ipsw)
select_ipsw_button.pack(pady=10)

nonce_pwned_button = tk.Button(root, text="Enter nonce pwnedDFU mode", command=run_turdusra1n_nonce)
nonce_pwned_button.pack(pady=10)

restore_ipsw_button = tk.Button(root, text="Restore", command=restore_turdus_merula_ipsw)
restore_ipsw_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

SHSH2 = ""
IPSW = ""

root.mainloop()
