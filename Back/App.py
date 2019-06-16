from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from DB1.database import Database

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

conn = Database(app=app, user='wout', password='wout', db='Project', host='localhost', port=3306)
print(conn)


def temperatuur():
    temperatuur_db = conn.get_data("Select Temperatuur from temperatuursensor ORDER BY MetingId Desc limit 1")
    for dictionary in temperatuur_db:
        for key, value in dictionary.items():
            temperatuur = value
            return temperatuur


def vochtigheid():
    vochtigheid_db = conn.get_data("Select Vochtigheid from vochtigheidssensor ORDER BY MetingId DESC limit 1")
    for dictionary in vochtigheid_db:
        for key, value in dictionary.items():
            vochtigheid = value
            return vochtigheid


def lichthoeveelheid():
    lichthoeveelheid_db = conn.get_data("Select `Hoeveelheid Licht` from lichtsensor ORDER BY MetingId DESC limit 1")
    for dictionary in lichthoeveelheid_db:
        for key, value in dictionary.items():
            lichthoeveelheid = value
            return lichthoeveelheid


def ideale_temperatuur():
    temperatuur_ideaal = conn.get_data("SELECT `Ideale Temperatuur` FROM planten WHERE Plantnaam = 'Kerstomaat'")
    for dictionary in temperatuur_ideaal:
        for key, value in dictionary.items():
            ideale_temperatuur = value
            return ideale_temperatuur


def ideale_vochtigheid():
    vochtigheid_ideaal = conn.get_data("SELECT `Ideale Vochtigheid` FROM planten WHERE Plantnaam = 'Kerstomaat' ")
    for dictionary in vochtigheid_ideaal:
        for key, value in dictionary.items():
            ideale_temperatuur = value
            return ideale_temperatuur


def ideale_lichthoeveelheid():
    lichthoeveelheid_ideaal = conn.get_data("SELECT `Ideale Lichthoeveelheid` FROM planten WHERE Plantnaam = 'Kerstomaat'")
    for dictionary in lichthoeveelheid_ideaal:
        for key, value in dictionary.items():
            ideale_temperatuur = value
            return ideale_temperatuur


licht_ideaal = ideale_lichthoeveelheid()
temp_ideaal = ideale_temperatuur()
vocht_ideaal = ideale_vochtigheid()
temp = temperatuur()
vocht = vochtigheid()
licht = lichthoeveelheid()


@app.route('/')
def hallo():
    return "Server is running"


@socketio.on("connect")
def connecting():
    global temp
    global vocht
    global licht
    global licht_ideaal
    global vocht_ideaal
    global temp_ideaal
    socketio.emit('temperatuur_ideaal', temp_ideaal)
    socketio.emit('vochtigheid_ideaal', vocht_ideaal)
    socketio.emit('lichthoeveelheid_ideaal', licht_ideaal)
    socketio.emit('temperatuur', temp)
    socketio.emit('vochtigheid', vocht)
    socketio.emit('lichthoeveelheid', licht)
    print("Connection with client established")


@socketio.on("nieuwe_data")
def data():
    temperatuur()
    vochtigheid()
    lichthoeveelheid()
    global temp
    global licht
    global vocht
    socketio.emit('temperatuur', temp)
    socketio.emit('vochtigheid', vocht)
    socketio.emit('lichthoeveelheid', licht)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)