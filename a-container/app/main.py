import sqlite3
from sqlalchemy import insert, true, exc
from sqlalchemy.dialects.sqlite import insert
from api import app
import sys
import json
import uuid
from flask import redirect, session
from flask import Flask, request, json, jsonify, Response, make_response, send_file, send_from_directory, render_template, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import importlib
from models import *
import os
import csv

# sys.path.append('../')
import pdfmaker.app.pdf_maker as pd
from upload.upload import make_thumb, chext, save_file, remove_files2, get_flist, get_dir_info
from werkzeug.security import generate_password_hash, check_password_hash
from csv_dir.csv_converter import upsert_csv, export_csv

# ------　ユーザー認証 -------
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.login_view = 'get_login'
login_manager.login_message = ""
login_manager.init_app(app)


class LoginUser(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return LoginUser(user_id)


@app.route('/')
@login_required
def home():
    return render_template('mw.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


def checkPassword(user_id, password):
    user = User.query.filter_by(name=user_id).first()
    if user:
        if user.password == password:
            return True
        pw_hash = user.password
        return check_password_hash(pw_hash, password)


@app.route('/login', methods=['POST'])
def login_post():
    user_id = request.form["userId"]
    password = request.form["password"]
    if checkPassword(user_id, password):
        user = LoginUser(user_id)
        login_user(user)
        newHistory = History(
            userName=user_id,
            modelName=None,
            modelId=None,
            action='login'
        )
        db.session.add(newHistory)
        db.session.commit()
        next = request.args.get('next')
        return redirect(next or '/')
    else:
        flash("ユーザーIDもしくはパスワードが間違っています")
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    try:
        newHistory = History(
            userName=current_user.id,
            modelName=None,
            modelId=None,
            action='logout'
        )
        db.session.add(newHistory)
        db.session.commit()
    except AttributeError as e:
        print(e)
        pass
    logout_user()
    # flash("ログアウトしました")

    return redirect('/')


@app.route('/is-session', methods=['GET'])
def is_session():
    if session.get('_id'):
        return jsonify({"session": True})
    else:
        return jsonify({"session": False})


@app.route('/on-click', methods=['GET'])
def onClick():
    return jsonify({"result": "UpdateSession", })


# ------　ユーザー認証ここまで -------


@app.route('/login-user', methods=['GET'])
def login_user_show():
    user = User.query.filter_by(name=current_user.id).first()
    return jsonify(UserSchema().dump(user))


@app.route('/test')
def test():
    return "Hello TEST!"


@app.route('/test-view-r')
def rootn():
    return app.send_static_file('test_view_r.html')


@app.route('/test-view-crud')
def crud_test():
    return app.send_static_file('test_view_crud.html')


@app.route('/test-view-crud2')
def crud_test2():
    return app.send_static_file('test_view_crud2.html')


@app.route('/test-view-crud3')
def crud_test3():
    return app.send_static_file('test_view_crud3.html')


@app.route('/test-view-crud4')
def crud_test4():
    return app.send_static_file('test_view_crud4.html')


@app.route('/test-view-crud5')
def crud_test5():
    return app.send_static_file('test_view_crud5.html')


@app.route('/test-view-invoice-switchable')
def crud_test_invoice_switchable():
    return app.send_static_file('test_view_invoice_switchable.html')


@app.route('/test-view-crud6')
def crud_test6():
    return app.send_static_file('test_view_crud6.html')


@app.route('/home-page')
def homePage():
    return render_template('home.html')


@app.route('/check-page')
@login_required
def checkPage():
    return render_template('check.html')


@app.route('/achievement-page')
@login_required
def chartPage():
    return render_template('achievement.html')


@app.route('/invoice-page')
@login_required
def invoicePage():
    return render_template('invoice.html')


@app.route('/quotation-page')
@login_required
def quotationPage():
    return render_template('quotation.html')


@app.route('/customer-page')
@login_required
def customerPage():
    return render_template('customer.html')


@app.route('/item-page')
@login_required
def itemPage():
    return render_template('item.html')


@app.route('/memo-page')
@login_required
def memoPage():
    return render_template('memo.html')

# ------pdf maker -------


@app.route('/pdfmaker', methods=["GET", "POST"])
def makepdf():

    if request.method == "GET":
        return redirect('/pdfmaker/data')
    elif request.method == "POST":
        d = request.json
        uuid_file_name = str(uuid.uuid1())+".pdf"
        alter_file_name = pd.pdf_maker(d, file_name=uuid_file_name)
        return alter_file_name


@app.route('/pdfmaker/<json_file>')
def makepdf_file(json_file):
    with open(f'./{json_file}.json', mode='r', encoding='utf-8') as f:
        d = json.load(f)

    uuid_file_name = str(uuid.uuid1())+".pdf"
    alter_file_name = pd.pdf_maker(d, file_name=uuid_file_name)

    # ------BytesIOを使えば、ファイル作成は必要ない(今回は使わない) ----
    # pdfdata = pdf_maker(d,is_BytesIO=True)
    # response = make_response(pdfdata)
    # response.mimetype = "application/pdf"
    # return response
    return alter_file_name


@app.route('/pdf/<file>', methods=["GET"])
def open_pdf(file):
    return app.send_static_file("pdf/"+file)


@app.route('/unit-page')
@login_required
def unitPage():
    return render_template('unit.html')


@app.route('/category-page')
@login_required
def categoryPage():
    return render_template('category.html')


@app.route('/maker-page')
@login_required
def makerPage():
    return render_template('maker.html')


@app.route('/setting-page')
@login_required
def settingPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "admin" or checkUser.role == "crescom_support":
            return render_template('setting.html')
    return redirect('/login')


@app.route('/crescom-support-page')
@login_required
def crescomSupportPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "crescom_support":
            return render_template('crescom_support_page.html')
    return redirect('/login')


@app.route('/csv-upload-page')
@login_required
def csvUploadPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "crescom_support":
            return render_template('csv_upload.html')
    return redirect('/login')


@app.route('/csv-download-page')
@login_required
def csvDownloadPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "crescom_support":
            return render_template('csv_download.html')
    return redirect('/login')


@app.route('/dust-select-page')
@login_required
def dustPage():
    return render_template('dust_select.html')


@app.route('/invoice-dust-page')
@login_required
def invoiceDustPage():
    return render_template('invoice_dust.html')


@app.route('/quotation-dust-page')
@login_required
def quotationDustPage():
    return render_template('quotation_dust.html')


@app.route('/user-page')
@login_required
def userPage():
    return render_template('user.html')


# --------- UPLOAD function ----------

up_base_dir = './static/'
static_dir = './static'
data_dir = './data'
up_dir = static_dir


def check_base_dir(base):
    if base == 's':
        return static_dir
    elif base == 'd':
        return data_dir
    else:
        return static_dir


@app.route('/test-upload')
def uptest():
    return render_template('./uptest.html')


@app.route("/upload-files/<base>/<path:dir_path>", methods=['POST'])
def upload_file(base, dir_path):
    if 'file' not in request.files:
        make_response(jsonify({'result': 'uploadFile is required.'}))
    f = request.files["file"]
    id = request.form['fileId']
    dir_path = check_base_dir(base)+"/" + dir_path
    return jsonify(save_file(id, dir_path, f))


@app.route("/delete-files/<base>", methods=['DELETE'])
def delete_files(base):
    base_dir = check_base_dir(base)
    dict_data = json.loads(request.data.decode())
    return jsonify(remove_files2(dict_data, base_dir))


@app.route("/list-files/<base>/<path:dir_path>", methods=['GET'])
def get_files_list(base, dir_path):
    # fid = dir_path.split('/')[-1]
    # return f" {fid} / {up_base_dir}{dir_path}"
    return jsonify(get_flist(check_base_dir(base), dir_path))


@app.route("/count-files/<base>/<path:dir_path>", methods=['GET'])
def get_files_count(base, dir_path):
    d_dict = {}
    for d in get_dir_info(check_base_dir(base), dir_path):
        d_dict[d['key']] = d['count_files']
    #print (d_dict)
    return jsonify(d_dict)


@app.route("/get-file/<path:path>", methods=['GET'])
def get_file(path):
    target = f"{up_dir}/{path}"
    if os.path.isfile(target):
        return send_file(target)
    else:
        return "File not found", 404

# ----- csv_upload_test -----


@app.route('/csv-test')
def CsvTest():
    return app.send_static_file('csv_test.html')


@app.route('/csv-import', methods=['POST'])
def CsvUpload():
    file = request.files['file']
    target = request.form['selected_import']
    file.save('csv_dir/import/'+target + '.csv')
    try:
        upsert_csv()
    except UnicodeDecodeError as e:
        print(e)
        return jsonify({"result": "error", "message": "UTF-8のみ利用可能です。UTF-8に変換されたCSVをインポートしてください。", "e_message": str(e)}), 500
    except (exc.IntegrityError, sqlite3.IntegrityError) as e:
        print(e)
        return jsonify({"result": "error", "message": "UNIQUEが重複しています。重複しない値を指定してください。", "e_message": str(e)}), 500
    except exc.CompileError as e:
        print(e)
        return jsonify({"result": "error", "message": "存在しないカラムがあります。対象となるテーブルとCSVのカラムを確認してください。", "e_message": str(e)}), 500
    except ValueError as e:
        print(e)
        return jsonify({"result": "error", "message": "不正な値があります。CSVに規格外または不要な空欄が無いか確認してください。", "e_message": str(e)}), 500
    except IndexError as e:
        print(e)
        return jsonify({"result": "error", "message": "インデックス数が不正です。CSVのヘッダーインデックスと値のインデックスを再確認してください。", "e_message": str(e)}), 500
    except exc.StatementError as e:
        print(e)
        return jsonify({"result": "error", "message": "値のデータ型エラーです。（Date型の入力は未対応）", "e_message": str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({"result": "error", "message": "予期せぬエラーが発生しました。", "e_message": str(e)}), 500
    else:
        return jsonify({"result": "ok", "message": "更新に成功しました"})
    finally:
        os.remove('csv_dir/import/'+target+'.csv')


# ----- csv_export -----


@app.route('/csv-export', methods=['GET'])
def CsvExport():
    export_csv()
    fixtures_dir = 'csv_dir/export/'
    downloadFileName = 'export.csv'
    downloadFile = fixtures_dir+'export.csv'

    return send_file(downloadFile, as_attachment=True,
                     download_name=downloadFileName,
                     mimetype='application/csv')

# ----- admin_db_init -----


@app.route('/db-init-page')
@login_required
def dbInitPage():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == "crescom_support":
            return render_template('db_init.html')
    return redirect('/login')


@app.route('/db-init', methods=["DELETE"])
@login_required
def dbInit():
    checkUser = User.query.filter_by(name=current_user.id).first()
    if checkUser:
        if checkUser.role == 'crescom_support':
            db.session.query(Customer).delete()
            db.session.query(Item).delete()
            db.session.query(Invoice).delete()
            db.session.query(Invoice_Item).delete()
            db.session.query(Invoice_Payment).delete()
            db.session.query(Quotation).delete()
            db.session.query(Quotation_Item).delete()
            db.session.query(Memo).delete()
            db.session.query(Unit).delete()
            db.session.query(Category).delete()
            db.session.query(Maker).delete()
            db.session.query(History).delete()
            db.session.commit()
            data = db.session.query(
                Customer, Item, Invoice, Invoice_Item, Invoice_Payment, Quotation, Quotation_Item, Memo, Unit, Category, Maker, History).all()
            return jsonify({"status": 200, "result": "ok", "data": data, "message": "データを全削除しました。"})
    return jsonify({"status": 403, "result": "権限エラー", "message": "権限がありません"})


@app.route('/mw')
@login_required
def mw():
    return render_template('mw.html')


@app.route('/mw2')
@login_required
def mw2():
    return render_template('mw2.html')


@app.route('/mw-menu')
@login_required
def mw_menu():
    return render_template('mw_menu.html')


@app.route('/leaflet')
@login_required
def leaflet():
    return render_template('leaflet.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5010, debug=True)
