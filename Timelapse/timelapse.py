from picamera import PiCamera
from os import system
import datetime
from time import sleep
dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
sleepinterval = 10
howmanypics= 1380
print(dateraw)
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

class data():
    pass

dates = data()
dates.dateList = []

for i in range(howmanypics):
    currentDateRaw = datetime.datetime.now()
    camera.capture('/home/pi/timelapse/photos/image{0:04d} ^{date}^.jpg'.format(i,date = currentDateRaw))
    dates.dateList.append(currentDateRaw) 
    sleep(sleepinterval)
    print("taking photos!",i)
    
    
  
camera.stop_preview()
print("Done taking photos!")

system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/timelapse/photos/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/timelapse/videos/{}.mp4'.format(30, datetimeformat))

print("Malfunction ")