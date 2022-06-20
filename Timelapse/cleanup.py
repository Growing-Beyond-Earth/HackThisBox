import os
import datetime

basePath = "/home/pi/timelapse/photos/"
fileList = []
cutOff = datetime.datetime(2022,6,3,1,32,46)
print(cutOff)
for entry in os.listdir(basePath):
    if os.path.isfile(os.path.join(basePath, entry)):
        print(entry)
        fileList.append(entry)

for entry in fileList:
    if (entry < cutOff):
        os.remove()