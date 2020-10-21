import time
import re

regex = r"(\+CGPSINFO: )[^\\]*"

gpsATBack = "+CGPSINFO: "

gpsATResponseNoSignal = "+CGPSINFO: ,,,,,,,,"

def ddmmToPureDeg (lat, NS, log, EW):
	ddLat = float(lat[:2]) # dd of lat
	mmLat = float(lat[2:]) # mm.mmmmmm of lat

	dddLog = float(log[:3]) # ddd of log
	mmLog = float(log[3:]) # mm.mmmmmm of log

	pureDegLat = round(((mmLat / 60) + ddLat) * (1 if NS == "N" else -1), 6)
	pureDegLog = round(((mmLog / 60) + dddLog) * (1 if EW == "E" else -1), 6)

	return [pureDegLat, pureDegLog]

def readGPSAT(serial, retries=2, waitInterval=0.05, timeout=3): # serial: serial object, retries: positive integer of number of times to retry, timeout: timeout of loop in seconds

	serial.write(("AT+CGPSINFO" + "\r\n").encode()) # included in read, as to read GPS data, must as for it

	firstTime = intervalTime = time.time()

	retryCount = 0

	while (((time.time() - firstTime) < timeout) and retryCount <= retries): # while the timeout has not expired and we have not run out of retries

		if (time.time() - intervalTime) > waitInterval:

			serWait = serial.inWaiting()

			if serWait:
				rawSerRead = serial.read(serWait)

				decodedSerRead = rawSerRead.decode()

				reprDecodedSerRead = repr(decodedSerRead)

				match = re.search(regex, reprDecodedSerRead)

				if match: # if the regex search method found a valid AT response for gps

					gpsATResponse = match.group() # actual AT response given back

					if gpsATResponse != gpsATResponseNoSignal: # if the gps AT response was not no signal
							
							#print(rawGPSData)
							gpsATResponseNoBack = gpsATResponse[len(gpsATBack):] # substring the full AT command giving back just the values, no back characters
							#print(gpsATResponseNoBack)
							gpsData = gpsATResponseNoBack.split(",") # gps data is now represented as an array/list

							return gpsData
					else: #else if there was a response of no signal
						return 0
				else: # else if there was an unexpected response / no gps data detected
					retryCount += 1
					intervalTime = time.time()

			intervalTime = time.time()

	return -1 # if after timing out or runnining through all retries and timing out, return no data recived