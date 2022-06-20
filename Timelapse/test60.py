from picamera import PiCamera
from os import system
import datetime
from time import sleep
dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
sleepinterval = 3

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

for i in range(60):
    camera.capture('/home/pi/timelapse/photos/image{0:04d}.jpg'.format(i))
    sleep(sleepinterval)
    print("taking photos!",i) 
    
  
camera.stop_preview()
print("Done taking 60 photos!")  

system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/timelapse/photos/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/timelapse/videos/{}.mp4'.format(30, datetimeformat))
