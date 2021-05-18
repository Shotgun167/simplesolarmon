# simplesolarmon
This is the simplest possible python script for monitoring a solar charge controller.  It queries the controller over the serial port using minimalmodbus, and dumps the data in an influxdB instance.  

Follow the default instructions for installing influxdB, and generate a token.  Replace <YOUR_TOKEN_HERE> in the code with what was generated.  If the script doesn't connect with your device, you might need to use a different USB port.  I was originally on 0, but moved to 1 during the development of this script.

You can install a Grafana instance to visualize data, but as I'm going to run this on a RaspberryPi Zero W, I want to save the memory space for data.  I'll just use the influxdb dashboards instead.

I bought an All-In_One controller from PowMr, and configured this software to it.  I have not yet discovered the correct register address for all the functions, but I have enough for basic monitory so far.  Your controller, if not from PowMr, will probably have the data stored in different registers.  If you're lucky, the manufacturer will not be stingy about sharing this information.  If you're not lucky, you can use the dump_register() and dump_registers() methods to scan through the registers till you find what you're looking for. PowMr sent me software that had some of the addresses in an ".ini" file.  The others I figured out by dumping the addresses and comparing that to the display.  That work continues.

As stated, I have a RaspberryPi Zero W on the way.  I will load it with Unbuntu and Influxdb.  Once configured, I will mount it below the controller and power it with pin-1 of the RS-485 port.  This is possible since the zero only draws 120mA.  This script will simply launch as the last step in the boot process.  If I find that data collection has been interrupted, I'll just power cycle it.
