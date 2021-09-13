import threading
import time
import modbus_poller
#import socket
import PID
import socketio
import datetime
import pandas as pd

def run_item(f, item):
    result_info = [threading.Event(), None]
    def runit():
        result_info[1] = f(item)
        result_info[0].set()
    threading.Thread(target=runit).start()
    return result_info

def gather_results(result_infos):
    results = [] 
    for i in range(len(result_infos)):
        result_infos[i][0].wait()
        results.append(result_infos[i][1])
    return results

class ModbusValue:
    def __init__(self, name, unitId, registers, scalefactor):
        self.name = name
        self.unitId = unitId
        self.registers = registers
        self.scalefactor = scalefactor

def proc(item):
    c = modbus_poller.initModbusDevice('84.9.41.168', 502, item.unitId, True)
    val = modbus_poller.getHoldingRegisterValue(c, item.registers[0], 1, item.scalefactor)
    return modbus_poller.convertToSignedInt(val[0])/item.scalefactor

#database connection details
# HOST = 'localhost'
# PORT = 9009
# sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialise WebSocket
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

#pid parameters
P = 1.4
I = 1
D = 0.001
pid = PID.PID(P,I,D)

#initialise system parameters
solar_inverter = ModbusValue('solar_inverter_W', 32, [1029], 1)
solar_charger = ModbusValue('solar_charger_W', 245, [789], 10)
ac_loads = ModbusValue('ac_loads_W', 100, [817], 1)
soc = ModbusValue('soc_W', 100, [843], 1)
chargeState = ModbusValue('soc_W', 100, [844], 1)
grid = ModbusValue('grid_W', 31, [2600], 1)
real_grid_sp = ModbusValue('real_grid_sp_W', 246, [37], 1)
battery = ModbusValue('battery', 100, [842], 1)
batteryVoltage = ModbusValue('battery', 100, [840], 10)
batteryCurrent = ModbusValue('battery', 100, [841], 10)
batteryTemperature = ModbusValue('battery', 225, [262], 10)


modbusDevices = [solar_inverter, solar_charger, ac_loads, grid, real_grid_sp, 
soc, chargeState, battery, batteryVoltage, batteryCurrent, batteryTemperature]
modbusValues = gather_results([run_item(proc, item) for item in modbusDevices])

propertyLoadW = modbusValues[2]
pVGenerationW = modbusValues[0] + modbusValues[1]
setPointW = propertyLoadW - pVGenerationW

feedback = 0
pid.SetPoint = setPointW
pid.setSampleTime(0.01)

try:
  #connect to database
  #sock.connect((HOST, PORT))
  
  i = 0
  while True:
    i = i + 1
    modbusValues = gather_results([run_item(proc, item) for item in modbusDevices])
    propertyLoadW = modbusValues[2] 
    pVGenerationW = modbusValues[0] + modbusValues[1]
    setPointW = propertyLoadW - pVGenerationW
    
    pid.update(feedback)
    output = pid.output
    
    feedback += (output - (1 / i))
  
    pid.SetPoint = setPointW
    
    #push readings to database
    #dataStr = gridImportExportW_real=' + str(modbusValues[3])
    
    timeNow = str(datetime.datetime.now())
    dataStr = { 'sensor':  [
        { 'name': 'propertyLoad', 'point': { 'timestamp': timeNow, 'value': str(propertyLoadW) } },
        { 'name': 'pVGeneration', 'point': { 'timestamp': timeNow, 'value': str(pVGenerationW) } },
        { 'name': 'setPointSimulated', 'point': { 'timestamp': timeNow, 'value': str(setPointW) } },
        { 'name': 'setPointReal', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[4]) } },
        { 'name': 'gridSimulated', 'point': { 'timestamp': timeNow, 'value': str(feedback) } },
        { 'name': 'gridReal', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[3]) } },
        { 'name': 'soc', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[5]) } },
        { 'name': 'chargeState', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[6]) }},
        { 'name': 'battery', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[7]) }},
        { 'name': 'batteryVoltage', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[8]) }},
        { 'name': 'batteryCurrent', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[9]) }},
        { 'name': 'batteryTemperature', 'point': { 'timestamp': timeNow, 'value': str(modbusValues[10]) }}
     ]} 


    currentTime= datetime.datetime.now()
    sio.emit('my message', {'data': dataStr })
    
    #sock.sendall(dataStr.encode())
    time.sleep(1)
        
except Exception as e:
    print("Got error: %s" % (e))


  















#simulated_grid_sp = ModbusDevice()
#print(gather_results([run_item(proc, item) for item in [1, 2, 10, 100]]))
