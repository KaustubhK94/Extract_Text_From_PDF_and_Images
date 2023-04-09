import pytesseract
from PIL import Image
from django.shortcuts import render
from pdf2image import convert_from_path
import os
from django.views.decorators.csrf import csrf_exempt

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def handle_uploaded_file(f):
    file_name = f.name
    with open('myapp/static/media/'+file_name,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_name

def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image, lang= 'eng')
    return extracted_text

def extract_text_from_pdf(pdf):
    pages = convert_from_path(pdf, last_page=5,poppler_path = r"C:\poppler-0.68.0\bin")
    text = ''
    for page in pages:
        text += str(extract_text_from_image(page))
    return text

def check_file(file_name):
    format = file_name.split(".",-1)[-1]
    file_path = os.path.join('myapp/static/media/',file_name)
    extract_text = None
    if format == 'jpg' or format == 'png' or format == 'jpeg':
        image = Image.open(file_path)
        extract_text = extract_text_from_image(image)
    elif format == 'pdf':
        extract_text = extract_text_from_pdf(file_path)
    return extract_text

@csrf_exempt
def upload_file(request):
    text = None
    if request.method == 'POST':
        file_name = handle_uploaded_file(request.FILES['upload_file'])
        text = check_file(file_name)
        if not text:
            extracted_text = "No text available to extract"
        else:
            extracted_text = "The extracted text is: " + text
        return render(request,'file_upload.html', {'text': extracted_text})
    return render(request,'file_upload.html')

