import os
import cv2
from uuid import uuid4
from flask import Flask, request, render_template, send_from_directory
from datetime import date
import datetime
import xlwt 
from xlwt import Workbook

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("Home.html")

@app.route("/upload", methods=["POST"])
def upload():
    nama  = request.form['nama']
    email = request.form['email']
    tanggal = str(date.today())
    
    target = os.path.join(APP_ROOT, 'images/')

    for upload in request.files.getlist("file"):
        filenames = upload.filename
        destination = "".join([target, filenames])
        upload.save(destination)
        
        image = cv2.imread(destination)
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        file_gray = filenames.replace(".", "_GRAY.")
        path_gray = "".join([target, file_gray])
        cv2.imwrite(path_gray, gray)

        blur = cv2.blur(image,(100,100))
        file_blur = filenames.replace(".", "_BLUR.")
        path_blur = "".join([target, file_blur])
        cv2.imwrite(path_blur, blur)

        edges = cv2.Canny(image,100,100)
        file_edge = filenames.replace(".", "_EDGE.")
        path_edge = "".join([target, file_edge])
        cv2.imwrite(path_edge, edges)

    
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1')

    sheet1.write(0, 0, 'Nama') 
    sheet1.write(0, 1, 'Email') 
    sheet1.write(0, 2, 'Tanggal')
    sheet1.write(0, 3, 'File RGB')
    sheet1.write(0, 4, 'File Gray')
    sheet1.write(0, 5, 'File Blur')
    sheet1.write(0, 6, 'File Edge')
    sheet1.write(1, 0, nama) 
    sheet1.write(1, 1, email) 
    sheet1.write(1, 2, tanggal)
    sheet1.write(1, 3, filenames)
    sheet1.write(1, 4, file_gray)
    sheet1.write(1, 5, file_blur)
    sheet1.write(1, 6, file_edge)

    wb.save(os.path.join(APP_ROOT, 'excel/'+nama+'.xls'))
        
    return render_template("Convert.html", a=nama,b=email,c=tanggal,image_name=filenames,image_gray=file_gray,image_blur=file_blur,image_edge=file_edge)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run(debug=True)
