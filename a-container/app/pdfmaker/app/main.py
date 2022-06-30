#
# Server sample for Pdf Maker  
#
from flask import Flask,make_response,redirect,request
from pdf_maker import pdf_maker
import json
import uuid
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def hello():
    return "Hello pdf server"

@app.route('/test')
def test():
    return app.send_static_file('test-pdf.html')

@app.route('/pdfmaker',methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def makepdf():

    if request.method == "GET":
        return redirect('/pdfmaker/data')
    elif request.method == "POST":
        d = request.json
        uuid_file_name = str(uuid.uuid1())+".pdf"
        alter_file_name = pdf_maker(d,file_name=uuid_file_name)
        return alter_file_name

@app.route('/pdfmaker/<json_file>')
@cross_origin(supports_credentials=True)
def makepdf_file(json_file):
    with open( f'./{json_file}.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    uuid_file_name = str(uuid.uuid1())+".pdf"
    alter_file_name = pdf_maker(d,file_name=uuid_file_name)

    #------BytesIOを使えば、ファイル作成は必要ない(今回は使わない) ----
    #pdfdata = pdf_maker(d,is_BytesIO=True)
    #response = make_response(pdfdata)
    #response.mimetype = "application/pdf"
    #return response
    return alter_file_name

@app.route('/pdf/<file>',methods=["GET"])
@cross_origin(supports_credentials=True)
def open_pdf(file):
    return app.send_static_file("pdf/"+file)
    
#----ファイルを指定してpdfのレスポンスを返す場合（今回は使わない）---
@app.route('/file/<file_name>')
@cross_origin(supports_credentials=True)
def file(file_name):
    try:
        with open( f"./pdf/{file_name}", mode='rb') as f:
            pdfdata = f.read()
            response = make_response(pdfdata)
            response.mimetype = "application/pdf"
            return response
    except:
        pass
        return f"file error:{file_name}"


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5020, debug=True)
