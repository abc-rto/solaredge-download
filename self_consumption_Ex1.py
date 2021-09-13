import threading
import time
import modbus_poller

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
    return modbus_poller.convertToSignedInt(val[0])

solar_inverter = ModbusValue('solar_inverter_W', 32, [1029], 1)
solar_charger = ModbusValue('solar_charger_W', 245, [789], 10)
ac_loads = ModbusValue('ac_loads_W', 100, [817], 1)
grid = ModbusValue('grid_W', 31, [2600], 1)
real_grid_sp = ModbusValue('real_grid_sp_W', 246, [37], 1)
modbusDevices = [solar_inverter, solar_charger, ac_loads, grid, real_grid_sp]

while True:
    print(gather_results([run_item(proc, item) for item in modbusDevices]))
    time.sleep(5)

#simulated_grid_sp = ModbusDevice()
#print(gather_results([run_item(proc, item) for item in [1, 2, 10, 100]]))