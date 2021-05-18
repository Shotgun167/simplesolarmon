"""
Driver for the PowMr Solar Controller using the Modbus RTU protocol
"""

import minimalmodbus
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 0.5


registers = {
    "Grid Voltage": {'register':531, 'multiplier':0.1, 'unit':'V'},
    "Grid Current": {'register':532, 'multiplier':0.1, 'unit':'A'},
    
    "Ambient Temperature": {'register':546, 'multiplier':0.1, 'unit':'C'},

    "PV Temperature": {'register':544, 'multiplier':0.1, 'unit':'C'},
    "Solar Voltage": {'register':263, 'multiplier':0.1, 'unit':'V'},
    "Solar Current": {'register':548, 'multiplier':0.1, 'unit':'A'},
    "Solar Power": {'register':265, 'multiplier':1, 'unit':'W'},
    
    "Battery Voltage": {'register':257, 'multiplier':0.1, 'unit':'V'},
    "Battery Current In": {'register':0, 'multiplier':1, 'unit':'A'},
    "Battery Power In": {'register':270, 'multiplier':0.1, 'unit':'W'},
    "Battery Current Out": {'register':0, 'multiplier':0.1, 'unit':'A'},
    "Battery Power Out": {'register':0, 'multiplier':1, 'unit':'W'},
    
    "Inv Temperature": {'register':545, 'multiplier':0.1, 'unit':'C'},
    "Inv Current": {'register':537, 'multiplier':0.1, 'unit':'A'},
    "Inv Voltage": {'register':534, 'multiplier':0.1, 'unit':'V'},
    "Inv VA": {'register':540, 'multiplier':1, 'unit':'VA'},
    "Inv Power": {'register':539, 'multiplier':1, 'unit':'W'}
}

class PowMr(minimalmodbus.Instrument):
    """
    Communicates using the Modbus RTU protocol (via provided USB<->RS232 cable)
    """

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)

    def dump_registers(self):
        for r in range(600):
            try:
                register = self.read_register(r)
                print(f"Register {r} \t=>  {register}")
            except:
                print(f"Register {r} \t=>   Exception")
                
    def dump_register(self, reg):
        try:
            register = self.read_register(reg)
            print(f"Register {reg} \t=>  {register}")
        except:
            print(f"Register {reg} \t=>   Exception")


    def full_report(self):
        for key, val in registers.items():
            try:
                measurement  = int(self.read_register(val['register'])) * val['multiplier']
                print(f"{key}: {measurement}{val['unit']}")
                time.sleep(.1)
            except Exception as e:
                print(e)

               
        
if __name__ == "__main__":
    # You can generate a Token from the "Tokens Tab" in the UI
    token = "<YOUR_TOKEN_HERE>"
    org = "home"
    bucket = "solar_controller"
    client = InfluxDBClient(url="http://localhost:8086", token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)


    powmr = PowMr('/dev/ttyUSB1', 1)
    while True:
        for key, val in registers.items():
            try:
                measurement  = int(powmr.read_register(val['register'])) * val['multiplier']
                write_api.write(bucket, org, Point("powmr").tag("host", "controller").field(key, measurement).time(datetime.utcnow(), WritePrecision.NS))
                time.sleep(1)
            except Exception as e:
                print(e)



# from solarshed.controllers.powmr import PowMr
# pow =  PowMr('/dev/ttyUSB1', 1)
# pow.dump_registers()
