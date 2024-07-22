import machine
import time

# red led and a green led
red = machine.Pin(14, machine.Pin.OUT)
green = machine.Pin(13, machine.Pin.OUT)


def main():
    try:
        while True:
            red.on()
            time.sleep(0.5)
            red.off()
            green.on()
            time.sleep(0.5)
            green.off()
    except Exception:
        # does not work yet
        red.off()
        print("Error or interrupt detected. LED turned off.")
