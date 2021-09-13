from pyModbusTCP.client import ModbusClient
from bitstring import BitArray, Bits


def initModbusDevice(host, port, unit_id, auto_open):
  try:
   c = ModbusClient(host, port, unit_id, auto_open=auto_open)
   #print('connected')
   return c
  except:
  # print('something went wrong')
   return None

def getHoldingRegisterValue(modbusClient, modbusRegister, length, scalefactor):
  regs = modbusClient.read_holding_registers(modbusRegister, length)
  if regs:
    return regs
  else:
    print("read error")
    return None
    
def convertToSignedInt(value):
  bits = Bits(bin=bin(value))
  bitString = bits.bin

  if len(bitString) != 16:
    for i in range(0, (16-len(bits))):
      bitString = str(0) + bitString

  b = BitArray(bin=bitString)
  #print(b.int)
  #print(b.int + b.int)
  return b.int


client = initModbusDevice("84.9.41.168", 502, 31, True)
regs = getHoldingRegisterValue(client, 2600, 1, 1)
#print(regs)
#convertToSignedInt(regs[0])


