# /

from fpdf import FPDF
pdf = FPDF()
imagelist = [f'pdfs/{i}.jpg' for i in range(1, 7)]
for image in imagelist:
    pdf.add_page()
    pdf.image(image,0, 0, 210, 297)
pdf.output("english.pdf", "F")