##
# Copyright (c) 2025, ilikesn0w 
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

def select_iboot():
    global iBoot
    iBoot = filedialog.askopenfilename(title="Select iBoot file", filetypes=[("iBoot files", "*.img4")])
    if iBoot:
        messagebox.showinfo("File Selected", f"You selected: {iBoot}")
    else:
        messagebox.showwarning("Error", "You didn't select a iBoot file")

def select_signed_sep():
    global signed_sep
    signed_sep = filedialog.askopenfilename(title="Select signed-SEP file", filetypes=[("Signed-SEP files", "*.img4")])
    if signed_sep:
        messagebox.showinfo("File Selected", f"You selected: {signed_sep}")
    else:
        messagebox.showwarning("Error", "You didn't select a signed-SEP file")
        
def select_target_sep():
    global target_sep
    target_sep = filedialog.askopenfilename(title="Select target-SEP file", filetypes=[("Target-SEP files", "*.im4p")])
    if target_sep:
        messagebox.showinfo("File Selected", f"You selected: {target_sep}")
    else:
        messagebox.showwarning("Error", "You didn't select a target-SEP file")

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

def restore_turdus_merula_ipsw():
    try:
        if not IPSW:
            messagebox.showerror("Error", "Please select IPSW file.")
            return

        merula_name = "turdus_merula"
        merula_path = "./bin/turdus_merula"

        if not os.path.isfile(merula_path):
            messagebox.showerror("Error", f"Executable file '{merula_name}' not found in ./bin")
            return

        process = subprocess.Popen([merula_path, "-o", IPSW],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def tethered_boot():
    try:
        if not iBoot or signed_sep or target_sep:
            messagebox.showerror("Error", "Please select a iBoot, signed-SEP and target-SEP files.")
            return

        turdusra1n_tethered_name = "turdusra1n"
        turdusra1n_tethered_path = "./bin/turdusra1n"

        if not os.path.isfile(turdusra1n_tethered_path):
            messagebox.showerror("Error", f"Executable file '{turdusra1n_tethered_name}' not found in ./bin")
            return

        process = subprocess.Popen([turdusra1n_tethered_path, "-t", iBoot, "-i", signed_sep, "-p", target_sep], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Turdus Merula GUI (A10(X) Tethered)")

perm_button = tk.Button(root, text="Fix permissions", command=fix_permissions)
perm_button.pack(pady=10)

pwned_button = tk.Button(root, text="Enter pwnedDFU mode", command=run_turdusra1n)
pwned_button.pack(pady=10)

select_ipsw_button = tk.Button(root, text="Select IPSW file", command=select_ipsw)
select_ipsw_button.pack(pady=10)

restore_ipsw_button = tk.Button(root, text="Restore", command=restore_turdus_merula_ipsw)
restore_ipsw_button.pack(pady=10)

select_iboot_button = tk.Button(root, text="Select iBoot file", command=select_iboot)
select_iboot_button.pack(pady=10)

select_signed_sep_button = tk.Button(root, text="Select signed-SEP file", command=select_signed_sep)
select_signed_sep_button.pack(pady=10)

select_target_sep_button = tk.Button(root, text="Select target-SEP file", command=select_target_sep)
select_target_sep_button.pack(pady=10)

tethered_boot_button = tk.Button(root, text="Tethered boot", command=tethered_boot)
tethered_boot_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

IPSW = ""
iBoot = ""
signed_sep = ""
target_sep = ""

root.mainloop()
