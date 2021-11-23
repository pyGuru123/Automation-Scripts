# Merge Multiple Images to A4 sized pdf
# pip install fpdf

from fpdf import FPDF

pdf = FPDF()
imagelist = [f'{i}.jpg' for i in range(1, 10)]
for image in imagelist:
    pdf.add_page()
    pdf.image(image, 0, 0, 210, 297)
pdf.output("output.pdf", "F")