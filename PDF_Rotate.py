import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
import matplotlib.pyplot as plt

def preview_pdf(file_path):
    images = convert_from_path(file_path)
    plt.imshow(images[0])
    plt.show()

def rotate_pdf(file_path, out_path, rotation_angle):
    # creating a pdf reader object
    pdfReader = PdfFileReader(file_path)

    # creating a pdf writer object for the new pdf
    pdfWriter = PdfFileWriter()

    # rotating each page
    for page in range(pdfReader.numPages):
        # creating rotated page object
        pageObj = pdfReader.getPage(page)
        pageObj.rotateClockwise(rotation_angle)

        # adding rotated page object to pdf writer
        pdfWriter.addPage(pageObj)

    # new pdf file object
    newFile = open(out_path, 'wb')

    # writing rotated pages to new file
    pdfWriter.write(newFile)

    # closing the new pdf file object
    newFile.close()

# Preview the PDF
file_path = 'path_to_your_pdf.pdf'
preview_pdf(file_path)

# Rotate the PDF
out_path = 'rotated_pdf.pdf'
rotation_angle = 90  # Specify the rotation angle here
rotate_pdf(file_path, out_path, rotation_angle)

# Preview the rotated PDF
preview_pdf(out_path)
