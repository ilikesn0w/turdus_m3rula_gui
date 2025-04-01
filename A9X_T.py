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

def select_shcblock():
    global SHCBLOCK
    SHCBLOCK = filedialog.askopenfilename(title="Select SHCBLOCK file", filetypes=[("SHCBLOCK files", "*.bin")])
    if SHCBLOCK:
        messagebox.showinfo("File Selected", f"You selected: {SHCBLOCK}")
    else:
        messagebox.showwarning("Error", "You didn't select a SHCBLOCK file")

def select_pteblock():
    global PTEBLOCK
    PTEBLOCK = filedialog.askopenfilename(title="Select PTEBLOCK file", filetypes=[("PTEBLOCK files", "*.bin")])
    if PTEBLOCK:
        messagebox.showinfo("File Selected", f"You selected: {PTEBLOCK}")
    else:
        messagebox.showwarning("Error", "You didn't select a PTEBLOCK file")

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

def run_turdus_merula_shcblock():
    try:
        if not IPSW:
            messagebox.showerror("Error", "Please select an IPSW file.")
            return

        merula_name = "turdus_merula"
        merula_path = "./bin/turdus_merula"

        if not os.path.isfile(merula_path):
            messagebox.showerror("Error", f"Executable file '{merula_name}' not found in ./bin")
            return

        process = subprocess.Popen([merula_path, "--get-shcblock", IPSW], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def run_turdus_merula_pteblock():
    try:
        if not SHCBLOCK:
            messagebox.showerror("Error", "Please select a SHCBLOCK file.")
            return

        merula_name = "turdus_merula"
        merula_path = "./bin/turdus_merula"

        if not os.path.isfile(merula_path):
            messagebox.showerror("Error", f"Executable file '{merula_name}' not found in ./bin")
            return

        process = subprocess.Popen([merula_path, "--get-pteblock", "--load-shcblock", SHCBLOCK, IPSW],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
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
        if not PTEBLOCK or not IPSW:
            messagebox.showerror("Error", "Please select both a PTEBLOCK and an IPSW file.")
            return

        merula_name = "turdus_merula"
        merula_path = "./bin/turdus_merula"

        if not os.path.isfile(merula_path):
            messagebox.showerror("Error", f"Executable file '{merula_name}' not found in ./bin")
            return

        process = subprocess.Popen([merula_path, "-o", "--load-pteblock", PTEBLOCK, IPSW],
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
        if not PTEBLOCK:
            messagebox.showerror("Error", "Please select a PTEBLOCK file.")
            return

        turdusra1n_tethered_name = "turdusra1n"
        turdusra1n_tethered_path = "./bin/turdusra1n"

        if not os.path.isfile(turdusra1n_tethered_path):
            messagebox.showerror("Error", f"Executable file '{turdusra1n_tethered_name}' not found in ./bin")
            return

        process = subprocess.Popen([turdusra1n_tethered_path, "-TP", PTEBLOCK], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        output_text.delete(1.0, tk.END)

        for line in process.stdout:
            formatted_line = re.sub(r'\x1b\[[0-9;]*m', '', process_log_line(line))
            output_text.insert(tk.END, formatted_line + "\n")
            output_text.see(tk.END)
            root.update()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.resizable(False, False)
root.title("Turdus Merula GUI (A9(X) Tethered)")

logo = tk.PhotoImage(file="./resources/png/Logo400x400.png")
logo_label = tk.Label(root, image=logo)
logo_label.place(x=135, y=0)

perm_button = tk.Button(root, text="Fix permissions", command=fix_permissions)
perm_button.pack(pady=10)

pwned_button = tk.Button(root, text="Enter pwnedDFU mode", command=run_turdusra1n)
pwned_button.pack(pady=10)

select_ipsw_button = tk.Button(root, text="Select IPSW file", command=select_ipsw)
select_ipsw_button.pack(pady=10)

backup_shcblock_button = tk.Button(root, text="Backup shcblock", command=run_turdus_merula_shcblock)
backup_shcblock_button.pack(pady=10)

select_shcblock_button = tk.Button(root, text="Select shcblock file", command=select_shcblock)
select_shcblock_button.pack(pady=10)

backup_pteblock_button = tk.Button(root, text="Backup pteblock", command=run_turdus_merula_pteblock)
backup_pteblock_button.pack(pady=10)

select_pteblock_button = tk.Button(root, text="Select pteblock file", command=select_pteblock)
select_pteblock_button.pack(pady=10)

restore_ipsw_button = tk.Button(root, text="Restore", command=restore_turdus_merula_ipsw)
restore_ipsw_button.pack(pady=10)

tethered_boot_button = tk.Button(root, text="Tethered boot", command=tethered_boot)
tethered_boot_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

IPSW = ""
SHCBLOCK = ""
PTEBLOCK = ""

root.mainloop()
