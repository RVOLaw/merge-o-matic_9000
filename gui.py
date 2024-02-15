import os
import tkinter as tk
import subprocess
from tkinter import filedialog
from threading import Thread
from pdf_utils import merge_pdfs  # Import merge_pdfs from pdf_utils

class PdfMergeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Merge-O-Matic 9000")

        self.status_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Input Folder Section
        self.input_folder_label = tk.Label(self.master, text="Input Folder:")
        self.input_folder_label.grid(row=0, column=0, sticky="e")

        self.input_folder_entry = tk.Entry(self.master, width=25)
        self.input_folder_entry.grid(row=0, column=1, padx=5, pady=5)

        self.input_folder_button = tk.Button(self.master, text="Browse", command=self.browse_input_folder)
        self.input_folder_button.grid(row=0, column=2, padx=5, pady=5)

        # Output Folder Section
        self.output_folder_label = tk.Label(self.master, text="Output Folder:")
        self.output_folder_label.grid(row=1, column=0, sticky="e")

        self.output_folder_entry = tk.Entry(self.master, width=25)
        self.output_folder_entry.grid(row=1, column=1, padx=5, pady=5)

        self.output_folder_button = tk.Button(self.master, text="Browse", command=self.browse_output_folder)
        self.output_folder_button.grid(row=1, column=2, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.start_merge, padx=10, pady=5)
        self.submit_button.grid(row=2, column=2, pady=10, padx=10)

        # Status Label
        self.status_label = tk.Label(self.master, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder_entry.delete(0, tk.END)
        self.input_folder_entry.insert(0, folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_entry.delete(0, tk.END)
        self.output_folder_entry.insert(0, folder_path)

    def start_merge(self):
        input_folder = self.input_folder_entry.get()
        output_folder = self.output_folder_entry.get()

        if not input_folder or not output_folder:
            tk.messagebox.showerror("Error", "Please provide both input and output folder paths.")
            return

        # Disable the submit button to prevent multiple submissions
        self.submit_button.config(state=tk.DISABLED)

        merge_thread = Thread(target=self.run_merge, args=(input_folder, output_folder))
        merge_thread.start()

    def run_merge(self, input_folder, output_folder):
        try:
            self.set_status("Processing...")
            merge_pdfs(input_folder, output_folder)
            self.set_status("PDFs merged successfully.")

            # Open file explorer and navigate into the output folder after successful merge
            subprocess.Popen(['explorer', '/e,', os.path.abspath(output_folder)], shell=True)
        except Exception as e:
            self.set_status(f"An error occurred: {str(e)}")
        finally:
            # Enable the submit button when the process is complete
            self.submit_button.config(state=tk.NORMAL)

    def set_status(self, message):
        self.status_var.set(message)
        self.master.update()
