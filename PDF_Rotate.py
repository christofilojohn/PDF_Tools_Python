import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path


class PDFRotator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PDF Rotator")

        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack()

        self.select_button = tk.Button(self.window, text="Select PDF", command=self.load_pdf)
        self.select_button.pack()

        self.rotate_right_button = tk.Button(self.window, text="Rotate Right", command=lambda: self.rotate_image(270))
        self.rotate_right_button.pack()

        self.rotate_left_button = tk.Button(self.window, text="Rotate Left", command=lambda: self.rotate_image(90))
        self.rotate_left_button.pack()

        self.done_button = tk.Button(self.window, text="Done", command=self.finalize_rotation)
        self.done_button.pack()

        self.pdf_path = None
        self.rotation_angle = 0
        self.pdf_image = None

    def load_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.rotation_angle = 0
            self.display_pdf(self.pdf_path)

    def rotate_image(self, angle):
        if self.pdf_image:
            self.rotation_angle = (self.rotation_angle + angle) % 360
            self.pdf_image = self.pdf_image.rotate(-angle)  # Negative for counter-clockwise rotation
            self.display_image(self.pdf_image)

    def finalize_rotation(self):
        if self.pdf_path and self.rotation_angle:
            self.rotate_pdf(self.rotation_angle)
            self.display_pdf(self.pdf_path)  # Resetting image to the original

    def rotate_pdf(self, angle):
        pdf_reader = PdfFileReader(self.pdf_path)
        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            page_obj = pdf_reader.getPage(page)
            page_obj.rotateClockwise(angle)
            pdf_writer.addPage(page_obj)

        out_path = "rotated_" + self.pdf_path
        with open(out_path, "wb") as out_file:
            pdf_writer.write(out_file)

        self.pdf_path = out_path

    def display_pdf(self, pdf_path):
        images = convert_from_path(pdf_path)
        self.pdf_image = images[0]
        self.display_image(self.pdf_image)

    def display_image(self, image):
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(300, 300, image=image)
        self.canvas.image = image

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    rotator = PDFRotator()
    rotator.run()
