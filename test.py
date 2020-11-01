"""
from pdf2image import convert_from_path
images = convert_from_path('files/ege2016.pdf', size=(3508, 2480))
images[0].save('files/img.png')
print(images)
"""
import datetime
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

import ghostscript

start = datetime.datetime.now()


def pdf2jpeg(pdf_input_path, jpeg_output_path):

    gs_call = "-q -sDEVICE=png16m -o {} -r300 {}".format(
        jpeg_output_path, pdf_input_path
    )

    gs_call = (
        "-dNumRenderingThreads=8 -dBufferSpace=2000000000 -dBandBufferSpace=500000000"
        + gs_call
    )
    print(gs_call)
    gs_call = gs_call.encode().split()

    ghostscript.Ghostscript(*gs_call)


def extract_pdf(input):
    pdf2jpeg(
        input,
        "ex.png",
    )


pdf_documents = ["files/ege2016.pdf"] * 30

# errror
# with ThreadPoolExecutor(4) as executor:
#    executor.map(extract_pdf, pdf_documents)

# gs -dNumRenderingThreads=8 -dBufferSpace=2000000000 -dBandBufferSpace=500000000-q -sDEVICE=png16m -o ex.png -r300 files/ege2016.pdf

with Pool(10) as p:
    p.map(extract_pdf, pdf_documents)

print(datetime.datetime.now() - start)
"""
convert           \
   -verbose       \
   -density 150   \
   -trim          \
    ege2016.pdf      \
   -quality 300   \
   -flatten       \
   -sharpen 0x1.0 \
    q.png
"""
