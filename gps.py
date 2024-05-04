# CPD spring 2024
# GPS code


from time import sleep
import serial

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def parseGPS(data):
    print(data, end='') 
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print("\nNo satellite data available.\n")
            return
        print("-----Parsing GPRMC-----")
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) 
        dirLat = sdata[4]     
        lon = decode(sdata[5]) 
        dirLon = sdata[6]      
        speed = sdata[7]       
        trCourse = sdata[8]    
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] 
        variation = sdata[10] 
        degreeChecksum = sdata[13] 
        dc = degreeChecksum.split("*")
        degree = dc[0]        
        checksum = dc[1]      

        latitude = lat.split() 
        longitute = lon.split() 

        print("\nLatitude: " + str(int(latitude[0]) + (float(latitude[2])/60)) + dirLat) 

        print("Longitute: " + str(int(longitute[0]) + (float(longitute[2])/60)) + dirLon)

        print("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s,True Course : %s, Date : %s, Magnetic Variation : %s(%s),Checksum : %s "%   (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum))

  
def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

print("Connecting Port..")
try:
    serw = serial.Serial(portwrite, baudrate=115200, timeout=1, rtscts=True, dsrdtr=True)
    serw.write('AT+QGPS=1\r'.encode())
    serw.close()
    sleep(1)
except Exception as e: 
    print("Serial port connection failed.")
    print(e)

print("Receiving GPS data\n")
ser = serial.Serial(port, baudrate=115200, timeout=0.5, rtscts=True, dsrdtr=True)
while True:
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting).decode('utf-8')
        print("Data received:", data)
    else:
        print("Waiting for data...")
    sleep(2)

