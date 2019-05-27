from django.contrib.auth import authenticate
from django.db import models
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import Usermodel


@api_view(["POST"])
def login(request):
    # try:
    #     from PIL import Image
    # except ImportError:
    #     import Image
    # import pytesseract

    # # If you don't have tesseract executable in your PATH, include the following:
    # pytesseract.pytesseract.tesseract_cmd = r'/home/yogesh_singh/lovekesh/lovekeshproject'
    # # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    #
    # # Simple image to string
    # imgtext = (pytesseract.image_to_string(Image.open('text.jpg')))
    # originaltext = ""
    # for k in imgtext:
    #     if k.isalnum() or k.isspace():
    #         originaltext+= k
    #
    # from fpdf import FPDF
    #
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_xy(0, 0)
    # pdf.set_font('arial', 'B', 13.0)
    # pdf.cell(ln=0, h=5.0, align='L', w=0, txt=originaltext , border=0)
    # pdf.output('test.pdf', 'F')
    #

    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = Usermodel.objects.get(username=username, password=password)
        return Response({'message': 'ok'},
                    status=HTTP_200_OK)
    except models.ObjectDoesNotExist:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None or username is "" or password is "":
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = Usermodel.objects.get_or_create(username=username, password=password)
        return Response({'message': 'ok'},
                    status=HTTP_200_OK)
    except models.ObjectDoesNotExist:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)

@api_view(["POST"])
def scan_qr(request):
    qrimg = request.FILES['img']
    from pyzbar import pyzbar
    from PIL import Image
    data = pyzbar.decode(Image.open(qrimg))
    qrdata = data[0].data
    return Response({'message': qrdata},
                    status=HTTP_200_OK)

@api_view(["POST"])
def img_to_text(request):
    img = request.FILES['img']
    try:
        from PIL import Image
    except ImportError:
        import Image
    import pytesseract
    imgtext = (pytesseract.image_to_string(Image.open(img)))
    originaltext = ""
    for k in imgtext:
        if k.isalnum() or k.isspace():
            originaltext += k

    file1 = open("text.csv", "w")
    file1.writelines(originaltext)
    file1.close()

    my_file = open('text.csv', 'rb').read()
    return HttpResponse(my_file, content_type="text/csv")
