import sys

from flask import Flask,request,json, jsonify,Response,make_response
#from flask_cors import CORS, cross_origin
import json
#from PIL import Image, ImageDraw, ImageFilter
from upload import make_thumb,chext,save_file,remove_files,get_flist #サムネイル作成関数

app = Flask(__name__)
#CORS(app, support_credentials=True)

@app.route("/")
@app.route('/test-upload')
def uptest():
    return app.send_static_file('./uptest.html')

@app.route("/upload",methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        make_response(jsonify({'result':'uploadFile is required.'}))
    f = request.files["file"]
    id= request.form['fileId'] 
    dir_path = "./static/upload" 
    return  jsonify(save_file(id,dir_path,f))

@app.route("/delete-files",methods=['DELETE'])
def delete_files():
    dict_data = json.loads(request.data.decode())
    return  jsonify(remove_files(dict_data))

@app.route("/file-list/<fid>",methods=['GET'])
def get_file_list(fid):

    return jsonify(get_flist(fid,"./static/upload"))

@app.route('/upload/<fid>/thumbs/<file>')
def upimage(fid,file):
    app.logger.debug(f"{fid}:{file}")
    return app.send_static_file(f'./upload/{fid}/thumbs/{file}')

@app.route('/<f>')
def proc(f):
    return app.send_static_file('./'+f)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5031)
    