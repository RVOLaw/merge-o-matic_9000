import tkinter as tk
import subprocess
import threading
import os
from tkinter import filedialog
from main import PDFMerger

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creditor Merger")

        self.input_label = tk.Label(root, text="Input Folder:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)

        self.input_entry = tk.Entry(root, width=25)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_input_button = tk.Button(root, text="Browse", command=self.browse_input_folder)
        self.browse_input_button.grid(row=0, column=2, padx=10, pady=10)

        self.output_label = tk.Label(root, text="Output Folder:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)

        self.output_entry = tk.Entry(root, width=25)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)

        self.browse_output_button = tk.Button(root, text="Browse", command=self.browse_output_folder)
        self.browse_output_button.grid(row=1, column=2, padx=10, pady=10)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.grid(row=2, column=2, padx=15, pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        # Bind the close window event to the method that interrupts the thread
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, folder_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folder_selected)
    
    def on_closing(self):
        # Stop the merging thread and close the application
        if hasattr(self, "merging_thread") and self.merging_thread.is_alive():
            self.merging_thread.do_run = False  # Set the flag to stop the thread
            self.merging_thread.join()  # Wait for the thread to finish
        self.root.destroy()

    def merge_pdfs(self):
        input_folder = self.input_entry.get()
        output_folder = self.output_entry.get()

        if input_folder and output_folder:
            # Disable the merge button during the process
            self.merge_button.config(state=tk.DISABLED)

            # Update the status label to inform the user that the request is processing
            self.status_label.config(text="Processing... Please wait.")

            # Start the merging process in a separate thread
            self.merging_thread = threading.Thread(target=self.merge_pdfs_thread, args=(input_folder, output_folder))
            self.merging_thread.start()

    def merge_pdfs_thread(self, input_folder, output_folder):
        try:
            pdf_merger = PDFMerger()
            pdf_merger.merge_pdfs(input_folder, output_folder)

            # Open file explorer and navigate into the output folder after successful merge
            subprocess.Popen(['explorer', '/e,', os.path.abspath(output_folder)], shell=True)

            # Update the status label in a thread-safe way
            self.root.after(0, self.status_label.config, {'text': "PDFs merged successfully."})
        except Exception as e:
            # Handle exceptions and update the status label
            self.root.after(0, self.status_label.config, {'text': f"Error: {str(e)}"})
        finally:
            # Enable the merge button after the process
            self.root.after(0, self.merge_button.config, {'state': tk.NORMAL})

if __name__ == "__main__":
    root = tk.Tk()
    gui = PDFMergerGUI(root)
    root.mainloop()