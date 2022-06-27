import time
import serial
import csv
ser=serial.Serial('/dev/ttyACM0',115200)
while True:
    try:
        readedText = ser.readline() #readline gets entire line of data until the end of file
        txtArr = readedText.split() #splits string into array
        with open('results.csv', 'a') as file: #opens the csv file the data will be added to. the 'a' indicates append,(cont)
            writer = csv.writer(file) #(cont) which adds the data to the end of the csv instead of creating a new one
            writer.writerow(txtArr) #write new row using the raw Pico data in txtArr
            time.sleep(2)
    except Exception as e:
        print("Exception: ", e) 
