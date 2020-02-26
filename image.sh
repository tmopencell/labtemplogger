#!/bin/bash
i="0"
while [ $i -lt 2 ] #This number controls iterations
do
DATE=$(date +"%Y-%m-%d-%H%M%S")
#echo "sleeping"
#sleep 1
# This takes a photo
sudo fswebcam -d /dev/video0 -r 352x288 --no-banner /home/pi/incubator/webcam/$DATE.jpg

#convert command (see imagemagik) to creat gifs
# The -delay gives the interval between picture changes and -loop sets it to repeat
sudo convert -delay 5 -loop 0 /home/pi/incubator/webcam/*.jpg /home/pi/incubator/webcam/timelapse.gif

 # Now we copy these gifs to the webstream folder  “../../var/www”
sudo cp /home/pi/incubator/webcam/$DATE.jpg /var/www/incubator/static.jpg
sudo cp /home/pi/incubator/webcam/timelapse.gif /var/www/incubator/timelapse.gif
i=$[$i+1]
echo $DATE, $i
done
sudo rm /home/pi/incubator/webcam/2019*.jpg
