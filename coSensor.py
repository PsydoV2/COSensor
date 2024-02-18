from machine import Pin, ADC, PWM
import utime

# Select ADC input 0 (GPIO26)
ADC_ConvertedValue = ADC(0)
DIN = Pin(16, Pin.IN) #D0 Pin
conversion_factor = 3.3 / (65535)

#Buzzer
buzzer = PWM(Pin(5)) #D1 Pin

# led_red
led_red = Pin(13, Pin.OUT) #D7 Pin
led_green = Pin(15, Pin.OUT) #D8 Pin


# Messen #############################################################################
def measure_R0():
    adc = ADC(0) #A0 Pin
    sensor_value_sum = 0

    utime.sleep(5)

    for _ in range(100):
        sensor_value_sum += adc.read_u16()

    sensor_value_avg = sensor_value_sum / 100.0
    sensor_volt = sensor_value_avg / 65535 * 3.3
    RS_air = (3.3 - sensor_volt) / sensor_volt
    R0 = RS_air / 6.5  # Der R0-Wert basiert auf dem Verhältnis RS/R0 = 6.5 in sauberer Luft

    return R0


def measure_co_gas_concentration(R0):
    sensor_value_sum = 0
    for _ in range(100):
        sensor_value_sum += ADC_ConvertedValue.read_u16()
    sensor_value_avg = sensor_value_sum / 100.0
    sensor_volt = sensor_value_avg * conversion_factor
    RS_gas = (3.3 - sensor_volt) / sensor_volt  # RL wird weggelassen
    ratio = RS_gas / R0  # Verhältnis RS/R0
    ppm = (ratio**(-2.769)) * 669.63  # Berechnung der Gas-Konzentration in ppm
    return ppm

# Alarm #############################################################################

def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)
    
def red_blink():
    led_red.on()
    utime.sleep(0.1)
    led_red.off()
    utime.sleep(0.001)
    
def alarm(frequency):
    playtone(frequency)
    red_blink()
    
def alarmoff():
    led_red.off()
    bequiet()
    
def warning():
    led_red.on()
    
def warningoff():
    led_red.off()
    
## CO Value dangerous
# Warning sound and red LED blinking
## CO Value unusually high
# Red LED blinking
## CO Value normal
# Green LED lit
    
def warmup():
    print("Warm up... ")
    
    for i in range(180):
        led_red.on()
        utime.sleep(0.5)
        led_red.off()
        led_green.on()
        utime.sleep(0.5)
        led_green.off()
    
#############
    
def main():

    valueNormal = 5 #Enter until which ppm Value it should be considered as normal
    valueHigh = 50 #Enter until which ppm Value it should be considered as suspicious but not dangerous


    warmup()
    
    while True:
        # When setting up the Sensor you have to calibrate the sensor
        # todo so you need the R0 value
        # you get the Value by executing the following line:

        # print("R0 Value: " , measure_R0())
        
        # Read the value and enter it in the Variable below
        R0_value = 0.163138
        # after that you can comment the line out again and your sensor is calibratet
    
        
        co_ppm = measure_co_gas_concentration(R0_value)
        
        print("CO Value: ", co_ppm, " ppm")
        
        if co_ppm < valueNormal:
            print("Value normal")
            led_green.on()
            alarmoff()
            warningoff()
        elif co_ppm < valueHigh:
            print("Value higher than normal")
            led_green.off()
            alarmoff()
            warning()
        else:
            print("Value dangerous")
            led_green.off()
            alarm(3200)
            warningoff()
            
        utime.sleep(0.5)

if __name__ == "__main__":
    main()




