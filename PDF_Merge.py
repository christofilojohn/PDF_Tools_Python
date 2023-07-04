import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfMerger
from tkinter import messagebox

class PDFMergerGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.title('PDF Merger')
        self.pdfs_to_merge = []

        self.merge_button = tk.Button(self.root, text='Merge PDFs', command=self.merge_pdfs)
        self.merge_button.pack()

        self.select_button = tk.Button(self.root, text='Select PDFs', command=self.select_pdfs)
        self.select_button.pack()

    def select_pdfs(self):
        self.pdfs_to_merge = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])
        
    def merge_pdfs(self):
        merger = PdfMerger()

        for pdf in self.pdfs_to_merge:
            merger.append(pdf)

        output_filename = filedialog.asksaveasfilename(defaultextension='.pdf')
        merger.write(output_filename)
        merger.close()

        self.pdfs_to_merge = []  # Clear the list

        messagebox.showinfo('Success', 'PDF files have been merged!')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PDFMergerGUI()
    app.run()
