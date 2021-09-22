import socketio
import time
import datetime
import random


# standard Python
sio = socketio.Client()

@sio.on('my message')
def on_message(data):
    print('I received a message!')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:8080')
print('my sid is', sio.sid)

while True:
    currentTime= datetime.datetime.now()
    sio.emit('my message', {'timestamp': str(currentTime), 'value': random.randint(1,101) })
    time.sleep(1)




