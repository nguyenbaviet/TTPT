from urllib import request

from flask import Flask, render_template, request, url_for, session
import main
from main import checkAuth
from werkzeug.utils import secure_filename
from os.path import join
from datetime import datetime
import secrets
from datetime import timedelta
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=3000000)

@app.route('/getPostInfor')
def getPostInfor():
    if(session.get('username')):
        a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
        id = a.count() + 1
        return render_template('postInfor.html', id=id)
    return render_template('login.html', errorr= False)

@app.route('/postInfor', methods=['GET', 'POST'])
def postInfor():
    if session.get('username'):
        if request.method == 'POST' and request.files['avatar']:
            img = request.files['avatar']
            img_name = secure_filename(img.filename)
            img_name = 'img_data/{}'.format(img_name)
            img.save(join('static', img_name))

            hoten = request.form['name']
            tenthuonggoi = request.form['nickname']
            ngaysinh = datetime.datetime.strptime(request.form['date1'], '%Y-%m-%d').strftime('%d/%m/%Y')
            gioitinh = request.form['gender']
            quequan = request.form['address1']
            dantoc = request.form['nation']
            tongiao = request.form['religion']
            quoctich = request.form['nationality']
            noisinh = request.form['noisinh']
            noithuongtru = request.form['address2']
            noiohientai = request.form['address3']
            nhommau = request.form['blood']
            sohochieu = request.form['passport']
            hotencha = request.form['namedad']
            hotenme = request.form['namemom']
            tinhtranghonnhan = request.form['relationship']
            hotenvochong = request.form['name1']
            hotencon = request.form['name2']

            a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
            cmt = a.post(hoten, img_name, tenthuonggoi, ngaysinh, gioitinh, quequan, dantoc, tongiao, quoctich, noisinh,
                         noithuongtru,
                         noiohientai, nhommau, sohochieu, hotencha, hotenme, tinhtranghonnhan, hotenvochong, hotencon)
            a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
            result = a.get(cmt)[-1]

            return render_template('postSuccess.html', result=result)
        a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
        id = a.count() + 1
        return render_template('postInfor.html', id=id)
    return render_template('login.html', error= False)

@app.route('/')
def getLogin():
    return render_template('login.html', error= False)
    # return render_template('showInfor1.html')
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', error= False)
@app.route('/index', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['tai-khoan']
        password = request.form['mat-khau']
        if(checkAuth(username, password)['statusCode'] == 0):
            session.permanent = True
            session['username'] = username
            session['password'] = password
            return render_template('showInfor.html', no_cmt=True)
        else:
            return render_template('login.html', error = True)
    return render_template('login.html', error= False)
@app.route('/getUpdate/<id>')
def getUpdate(id):
    if session.get('username'):
        a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
        result = a.get(id)[-1]
        return render_template('updateInfor.html', result=result)
    return render_template('login.html', error= False)

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    if session.get('username'):
        if request.method == 'POST':
            a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
            result = a.get(id)[-1]
            tenthuonggoi = request.form['nickname']
            ngaymat = ''
            noiohientai = request.form['address3']
            sohochieu = request.form['passport']
            tinhtranghonnhan = request.form['relationship']
            hotenvochong = request.form['name1']
            hotencon = request.form['name2']

            a.post(result['hoten'], result['anh'], tenthuonggoi, result['ngaysinh'], result['gioitinh'],
                   result['quequan'], result['dantoc'], result['tongiao'], result['quoctich'], result['noisinh'],
                   result['noithuongtru'], noiohientai, result['nhommau'], sohochieu, result['hotencha'],
                   result['hotenme'],
                   tinhtranghonnhan, hotenvochong, hotencon, ngaymat, result['cmt'])
            a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
            result = a.get(id)[-1]
            return render_template('postSuccess.html', result=result)
    return render_template('login.html', error= False)

@app.route('/getInfor', methods=['GET', 'POST'])
def getInfor():
    if session.get('username'):
        a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
        if request.method == 'GET':
            return render_template('showInfor.html', no_cmt=True)
        elif request.method == 'POST':
            result = a.get(request.form['cmt'])
            if len(result) == 0:
                return render_template('showInfor.html', no_cmt=True)
            result = result[-1]
        return render_template('showInfor.html', result=result, no_cmt=False)
    return render_template('login.html', error= False)

@app.route('/getHistory', methods = ['GET', 'POST'])
def getHistory():
    if session.get('username'):
        if request.method == 'GET':
            return render_template('history.html', no_cmt= True)
        elif request.method == 'POST':
            a = main.V_chainAPIs(session['username'], session['password'], 'MANAGER')
            results = a.get(request.form['cmt'])
            if(len(results) == 0):
                return render_template('history.html', no_cmt= True)
            elif len(results) == 1:
                return render_template('history.html', no_update = True, no_cmt = False)
            else:
                result = results[-1]
                new_result = []
                temp = len(results) - 1
                while temp > 0:
                    results[temp - 1]['timestamp'] = datetime.datetime.fromtimestamp(results[temp - 1]['timestamp']).strftime('%d/%m/%Y')
                    temp -= 1
                    new_result.append(results[temp])
                return render_template('history.html', no_update = False, no_cmt = False, results= new_result, result= result)
    return render_template('login.html', error= False)


@app.route('/test')
def test():
    return render_template('postInfor.html')
if __name__ == '__main__':
    app.run(debug=True)
