import SIM7600XGPS
import serial
import time

ser = serial.Serial('/dev/ttyUSB3',115200)
ser.flushInput()


try: 
	while True:
		gps = SIM7600XGPS.readGPSAT(ser)

		if gps != -1:
			if gps != 0:
				print("Raw GPS data: \n")
				print(gps)

				print("Pure Degree Lat and Log: \n")
				lat, log = SIM7600XGPS.ddmmToPureDeg(gps[0], gps[1], gps[2], gps[3])

				print("Pure degrees position: " + lat + ", " + log)
			else:
				print("No GPS signal")
		else:
			print("no gps data read (nothing reading from port?)")
		time.sleep(5)

except KeyboardInterrupt:
	print("stopping....")
	ser.close()