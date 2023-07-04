import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path

class PDFRotateThread(QThread):
    rotation_done = pyqtSignal(str)

    def __init__(self, pdf_path, rotation_angle):
        super().__init__()
        self.pdf_path = pdf_path
        self.rotation_angle = rotation_angle

    def run(self):
        pdf_reader = PdfFileReader(self.pdf_path)
        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):
            page_obj = pdf_reader.getPage(page)
            page_obj.rotateClockwise(self.rotation_angle)
            pdf_writer.addPage(page_obj)

        out_path = "rotated_" + self.pdf_path
        with open(out_path, "wb") as out_file:
            pdf_writer.write(out_file)

        self.rotation_done.emit(out_path)


class PDFRotator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Rotator")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.select_button = QPushButton("Select PDF")
        self.select_button.clicked.connect(self.load_pdf)
        self.layout.addWidget(self.select_button)

        self.rotate_right_button = QPushButton("Rotate Right")
        self.rotate_right_button.clicked.connect(lambda: self.rotate_image(270))
        self.layout.addWidget(self.rotate_right_button)

        self.rotate_left_button = QPushButton("Rotate Left")
        self.rotate_left_button.clicked.connect(lambda: self.rotate_image(90))
        self.layout.addWidget(self.rotate_left_button)

        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.finalize_rotation)
        self.layout.addWidget(self.done_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.pdf_path = None
        self.rotation_angle = 0
        self.pdf_image = None

    def load_pdf(self):
        self.pdf_path, _ = QFileDialog.getOpenFileName(None, "Select PDF", "", "PDF files (*.pdf)")
        if self.pdf_path:
            self.rotation_angle = 0
            self.progress_dialog = QProgressDialog("Loading PDF...", "", 0, 0, self)
            self.progress_dialog.setCancelButton(None)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.show()
            QApplication.processEvents()
            self.display_pdf(self.pdf_path)

    def rotate_image(self, angle):
        if self.pdf_image:
            self.rotation_angle = (self.rotation_angle + angle) % 360
            self.pdf_image = self.pdf_image.rotate(-angle)  # Negative for counter-clockwise rotation
            self.display_image(self.pdf_image)

    def finalize_rotation(self):
        if self.pdf_path and self.rotation_angle:
            self.thread = PDFRotateThread(self.pdf_path, self.rotation_angle)
            self.thread.rotation_done.connect(self.rotation_finished)
            self.thread.start()

    def rotation_finished(self, rotated_path):
        self.pdf_path = rotated_path
        self.display_pdf(rotated_path)

    def display_pdf(self, pdf_path):
        images = convert_from_path(pdf_path)
        self.pdf_image = images[0]
        self.display_image(self.pdf_image)
        self.progress_dialog.close()

    def display_image(self, image):
        qim = ImageQt(image).copy()
        pix = QPixmap.fromImage(qim)
        self.image_label.setPixmap(pix)


def main():
    app = QApplication(sys.argv)
    rotator = PDFRotator()
    rotator.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
