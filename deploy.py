import os
from flask import Flask, render_template, request, abort, send_file
from flask_socketio import SocketIO, emit, send
port = int(os.environ.get("PORT", 5000))

passwordTxt = open("files/password.txt", "r").read()
controllPanelHTML = open("templates/controllPanel.html","r").read()
explanationHTML = open("templates/explanation.html","r").read()
loginHTML = open("templates/login.html","r").read()
mainTextHTML = open("templates/mainText.html","r").read()
robotOfflineHTML = open("templates/robotOffline.html","r").read()
errorHTML = open("templates/error.html","r").read()

connectUser = ""
robotId = ""

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/ArTarumianBarak-Regular-8925.ttf')
def sendingFuckinFile():
	return send_file("files/ArTarumianBarak-Regular-8925.ttf", mimetype='image/gif')

@app.route('/MoreThanEnough.ttf')
def sendingFuckinFile4():
	return send_file("files/MoreThanEnough.ttf", mimetype='image/gif')


@app.route('/bakcground.jpg')
def sendingFuckinFile2():
	return send_file("files/bakcground.jpg", mimetype='image/gif')

@app.route('/logo.png')
def sendingFuckinFile3():
	return send_file("files/logo.png", mimetype='image/gif')

@socketio.on_error()
def error_handler(e):
    print(e)

@socketio.on('connect')
def helo():
	if robotId != "":
		if connectUser != "":
			emit('mainDivHtml',explanationHTML+mainTextHTML,room = request.sid)
		else:
			emit('mainDivHtml',loginHTML+mainTextHTML,room = request.sid)
	else:
		emit('mainDivHtml',robotOfflineHTML+mainTextHTML,room = request.sid)

@socketio.on('reviewOfPasswrd')
def reviewOfPasswrd(password):
	if passwordTxt == password:
		json = {
			'textHTML':explanationHTML+mainTextHTML,
			'id':request.sid
		}
		emit('mainDivHtml',controllPanelHTML,room = request.sid)
		socketio.emit('alreadyConnected',json)
		global connectUser
		connectUser = request.sid
	else:
		emit('false','You are input false passwordTxt',room = request.sid)

@socketio.on('move')
def move(json):
	if request.sid==connectUser:
		if robotId!="":
			emit('move',json,room = robotId)
		else:
			emit('mainDivHtml',robotOfflineHTML,room = request.sid)
	else:
		emit('mainDivHtml',errorHTML,room = request.sid)

@socketio.on('robotConnect')
def robotConnect(password):
	if passwordTxt==password:
		emit('connectedInServer',connectUser,room = request.sid)
		socketio.emit('mainDivHtml',loginHTML+mainTextHTML)
		global robotId
		robotId = request.sid

@socketio.on('webCam')
def webCam(image):
	if request.sid==robotId:
		emit('webCamB',image,room = connectUser)

@socketio.on('disconnect')
def helo():
	global connectUser
	global robotId
	if request.sid == connectUser:
		connectUser = ""
		socketio.emit('mainDivHtml',loginHTML+mainTextHTML)
	elif request.sid == robotId:
		robotId = ""
		socketio.emit('robotConnection',False)
	else:
		print("disconnected->id="+request.sid)

if __name__=='__main__':
	socketio.run(app, host='0.0.0.0', port=port)
print(port+socketio.async_mode)