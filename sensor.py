from gpiozero import MotionSensor, Button, Buzzer
from datetime import datetime, timedelta
from time import sleep 
import subprocess

motionSensor = MotionSensor(23) # these will be changed for actual GPIO pins
button = Button(13)
buzzer = Buzzer(15)

# dates captured images
def captureImage():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    imagePath = f"motion_capture_{timestamp}.jpg"
    print(f"Capturing Image: {imagePath}")

    # send to SQL database to then send to phone ?

    # calls the face detection py
    subprocess.run(['python', 'faceDetection.py', imagePath])

# initialize variables
motion_start_time = None


# function for checking if motion has been detected or button is pushed
try: 
    print("Motion detection system is active. Press Crtl+C to exit.")

    # function will now only take a photo if individual is within the sensor for more than 10 seconds
    while True:
        if motionSensor.motion_detected:
            if motion_start_time is None:
                motion_start_time = datetime.now()
                print("Motion Detected!")
            else:
                if datetime.now() - motion_start_time > timedelta(seconds=10):
                    print("Motion Detected for more than 10 secounds!")
                    captureImage()
                    motion_start_time = None

        else: 
            motion_start_time = None

        # when button is pressed it will take a photo, then sleep
        if button.is_pressed: 
            print("Button Pressed!")
            captureImage()
            # buzzer is played when button is pressed
            buzzer.on() 
            sleep(0.5)
            buzzer.off()
            
        sleep(10)

except KeyboardInterrupt:
    print("Motion detection system stopped.") 

finally: 
    motionSensor.close()
    button.close()