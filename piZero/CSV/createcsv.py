import time
import serial
import csv
ser=serial.Serial('/dev/ttyACM0',115200)
while True:
    try:
        readedText = ser.readline() #readline gets entire line of data until the end of file
        txtArr = readedText.split() #splits string into array
        with open('results.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(txtArr)
            time.sleep(2)
    except Exception as e:
        print("Exception: ", e)
                    

            
  

