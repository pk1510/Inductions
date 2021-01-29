import time, msvcrt, serial
mySerial = serial.Serial('com4', 9600)
values = []
while True:
    inp = str(input())
    if(inp == 'S'):
        mySerial.write('S'.encode())
        while(mySerial.inWaiting() >0 and readInput() != 'E'):  #input() waits for infinite time
            values.append(mySerial.readline())
        mySerial.write("E".encode())
        print(values)

def readInput(timeout = 0.5):   #waits only for half a second
    start_time = time.time()
    input = ''
    while ((time.time() - start_time) < timeout):
        if msvcrt.kbhit():    #returns True if a keyboard button is hit
            response = msvcrt.getch().decode('ASCII')  #decode from binary
            input = response
    return input
