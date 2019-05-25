#Libraries to import
import RPi.GPIO as GPIO
import time

#Set LED Pin
LED = 13


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)


pwm_led = GPIO.PWM(LED, 50)
pwm_led.start(100)
max_distance = 100


#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24


#set GPIO direction (IN/OUT
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def distance():
    #set TRIGGER High
    GPIO.output(GPIO_TRIGGER, True)
    
    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    #save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()


    #save time of  arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()


    #time difference between start and arrival 
    TimeElapsed = StopTime - StartTime 
    #multiply with the sonic speed (34300 cm/s)
    #and divide by 2, because there an back
    distance = (TimeElapsed * 34300) / 2
    
    return distance 

if __name__ == '__main__':
    try:
        #test the LED to make sure it fades correctly
        print("testing LED")
        for x in range(100):
            pwm_led.ChangeDutyCycle(x)
            time.sleep(0.02)
            
        for x in range(100):
            pwm_led.ChangeDutyCycle(100-x)
            time.sleep(0.02)
        
        print("testing LED DONE")
        while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            #measure the distance and adjust the brightness accordingly
            clampedValue = clamp(dist/max_distance, 0, 1)
            LedDutyCycle = (1 - clampedValue) * 100
            print(str(LedDutyCycle))
            pwm_led.ChangeDutyCycle(LedDutyCycle)
                
            time.sleep(0.1)
        
        #Reset by pressing CTRL+C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

