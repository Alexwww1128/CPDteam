///////////////////////////////////////////////////////////////////////////////
//                   ALL STUDENTS COMPLETE THESE SECTIONS
// Title:              (program's title)
// Files:              (list of source files)
// Quarter:            (course) Spring 2020
//
// Author:             (your name)
// Email:              (your email address)
// Instructor's Name:  (name of your instructor)
//
//////////////////// PAIR PROGRAMMERS COMPLETE THIS SECTION ///////////////////
//
//                  CHECK ASSIGNMENT PAGE TO see IF PAIR-PROGRAMMING IS ALLOWED
//                  If pair programming is allowed:
//                  1. Read PAIR-PROGRAMMING policy
//                  2. Choose a partner wisely
//                  3. Complete this section for each program file
//
// Pair Partner:        (name of your pair programming partner)
// Email:               (email address of your programming partner)
// Instructors's Name:  (name of your partner's instructor)
// Lab Section:         (your partner's lab section number)
//
//////////////////// STUDENTS WHO GET HELP FROM OTHER THAN THEIR PARTNER //////
//                   must fully acknowledge and credit those sources of help.
//                   Instructors and TAs do not have to be credited here,
//                   but roommates, relatives, strangers, etc do.
//
// Persons:          Identify persons by name, relationship to you, and email.
//                   Describe in detail the the ideas and help they provided.
//
// Online sources:   Avoid web searches to solve your problems, but if you do
//                   search, be sure to include Web URLs and description of
//                   of any information you find.
//////////////////////////// 80 columns wide //////////////////////////////////



from time import sleep
import serial

portwrite = "/dev/ttyUSB2"
port = "/dev/ttyUSB1"

def parseGPS(data):
    print(data, end='') #prints raw data
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print("\nNo satellite data available.\n")
            return
        print("-----Parsing GPRMC-----")
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
        variation = sdata[10]  #variation
        degreeChecksum = sdata[13] #Checksum
        dc = degreeChecksum.split("*")
        degree = dc[0]        #degree
        checksum = dc[1]      #checksum

        latitude = lat.split() # parsing latitude
        longitute = lon.split() # parsing longitute

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
    serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
    serw.write('AT+QGPS=1\r'.encode())
    serw.close()
    sleep(1)
except Exception as e: 
    print("Serial port connection failed.")
    print(e)

print("Receiving GPS data\n")
ser = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)
while True:
   data = ser.readline().decode('utf-8')
   parseGPS(data)
   sleep(2)
