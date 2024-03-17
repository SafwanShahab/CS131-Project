#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse
import yagmail
import time

from geopy.geocoders import Nominatim
from datetime import datetime
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput,saveImage, Log


prev_time = time.time()

def time_check(cur_time):
  global prev_time
  if(cur_time - prev_time >= 30):
    prev_time = cur_time
    return True
  else:
    return False

def email_alert(intruders, timestamp, location):
  #initializing email
  yag = yagmail.SMTP(user='jetsonsecsys@gmail.com', password='crhboaphzpdiuiph')
  #compse the message
  subject = 'Interuder Alert'
  image_path = f"my_image.jpg"
  body = f'''
  One or more intruders were detected at {location}.

  Report:
  - No of trespassers: {intruders}
  - Timestamp: {timestamp}
  Please see attached photo:
  '''
  to_email = 'lmcgu004@ucr.edu'
  yag.send(to=to_email, subject=subject, contents=body, attachments=image_path)
  yag.close()

def text_alert():
  #initializing email
  yag = yagmail.SMTP(user='jetsonsecsys@gmail.com', password='crhboaphzpdiuiph')
  #compse the message
  subject = 'From Jetson Security System'
  body = 'An intruder has been detected. Check your email for more details'
  to_sms = '9513758285@tmomail.net'
  yag.send(to=to_sms, subject=subject, contents=body)
  yag.close()

geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode("Statue of Liberty, New York")
address = location.address
latitiude = location.latitude
longitude = location.longitude



#clear the outputfile
with open('output.txt', 'w') as f:
  pass

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
  args = parser.parse_known_args()[0]
except:
  print("")
  parser.print_help()
  sys.exit(0)

# create video sources and outputs
input = videoSource("/dev/video0")      # '/dev/video0' for V4L2
output = videoOutput(args.output, argv=sys.argv)



# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# process frames until EOS or the user exits
filename = 'image.jpg'

output_uri = f'file://{filename}'


while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))
    people = []
    for detection in detections:
      if(detection.ClassID == 1):
        people.append(detection.ClassID)
        saveImage(f"my_image.jpg", img)
    if(time_check(time.time()) is True and len(people) > 0):
      videoOutput(output_uri, img)
      with open('output.txt', 'a') as f:
        num_people = len(people)
        #Write the number of people in the image to the output file
        if(num_people > 1):
          email_alert(num_people, datetime.now(), str(address))
          text_alert()
          videoOutput(output_uri, img)
          last_alert = time.time()
          f.write(str(num_people) + " people were detected in the secure area.\n")
          #Time and date
          f.write("---------------------------------------\n")
          f.write("Time of detection:\n")
          f.write("-------------------\n")
          f.write(str(datetime.now()) + "\n")
          #Location information
          f.write("---------------------------------------\n")
          f.write("Location Information:\n")
          f.write("-------------------\n")
          f.write("Location: " + str(address) + "\n")
          f.write("Latitude: " + str(latitiude) + "\n")
          f.write("Longitude: " + str(longitude) + "\n")
          f.write("-----------------------------------------------------------------------------\n")
          f.write("                                                                             \n")


        elif(num_people == 1):
          email_alert(num_people, datetime.now(), str(address))
          text_alert()
          saveImage(f"my_image.jpg", img)
          last_alert = time.time()
          f.write(str(num_people) + " person was detected in the secure area.\n")
          #Time and date
          f.write("---------------------------------------\n")
          f.write("Time of detection:\n")
          f.write("-------------------\n")
          f.write(str(datetime.now()) + "\n")
          #Location information
          f.write("---------------------------------------\n")
          f.write("Location Information:\n")
          f.write("-------------------\n")
          f.write("Location: " + str(address) + "\n")
          f.write("Latitude: " + str(latitiude) + "\n")
          f.write("Longitude: " + str(longitude) + "\n")
          f.write("-----------------------------------------------------------------------------\n")
          f.write("                                                                             \n")

      people.clear()


      # Write the data contained in 'detection' to the file
      #f.write(str(detection) + "\n")

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
