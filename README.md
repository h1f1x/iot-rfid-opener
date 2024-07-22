# Building a RFID reader with ESP32

This project is a simple RFID reader that sends a message to a phone number when a card is detected. The project uses an ESP32 and a MFRC522 RFID reader. The code is written in Micropython and uses the Twilio API to send the message.

Why you might ask? 

I wanted to learn more about using Microcontroller and iot to create digital twins to automate and monitor.
The real showcase would be to use this RFID reader to open a gate. As the gate is controlled by an RTU5024 GSM gate opener, I could use send a message to the gate opener to open the gate.

## Overview and Status

The project is still in the exploring and learning phase. At that point, I have the following components working or knowledge is acquired:

- [x] ESP32 connected to the Mac through USB (and I can access it)
- [x] How to install Micropython on the ESP32
- [x] MFRC522 RFID reader connected to the ESP32
- [x] Micropython code to read the RFID card
- [ ] Twilio API to send a message
- [ ] How to do logging in Micropython
- [ ] OTA updates of the ESP32
- [ ] Handling secrets 

Something which would be nice to have and a standard to me:
- [x] Deploy the code to the ESP32 with a single command
- [x] Run and Debug the code
- [ ] Dockerize the development environment

Bare with me, if something is not complete or not working. I will update the README as I progress. The main goal is to make it reproducible and easy to understand. Maybe it will help someone else to get started with Micropython and ESP32.

### Hardware

- ESP32 Wroom-32 (DevKitC ?!) from AZDelivery
- MFRC522 RFID reader
- Mac with Intel processor

## Setup

Something you might need to install:

- just (install with `brew install just`)

### USB to UART (onetimer)

Install the driver in order to communicate UART through USB.
https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Here some maybe useful commands:

```
ioreg -p IOUSB

```

find the dev with:
``` 
ls /dev/cu.*
```


### ESP32 firmware flashing (onetimer)

Erase the flash memory:
```
esptool.py --chip esp32 --port $SERIAL_PORT erase_flash
```

Flashing the firmware with Micropython (see below) (ESP32_GENERIC-OTA-20240602-v1.23.0.bin):
```
esptool.py --chip esp32 --port $SERIAL_PORT --baud 460800 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC-OTA-20240602-v1.23.0.bin
```

## Micropython

https://docs.micropython.org/en/latest/

ESP32 Quick reference: https://docs.micropython.org/en/latest/esp32/quickref.html

### Setup

This will be handled by the `justfile`.

Some additional python packages might be needed:
```
pip install mpfshell
```

### Gists

Execute any python direclty from the terminal:
```
pyboard.py --device $SERIAL_PORT -c 'print(1+1)'
```

https://docs.micropython.org/en/latest/reference/mpremote.html

```
mpremote 
```

```
mip.install("http://example.com/x/y/foo.py")
```


## RFID MFRC522 und the ESP32

PINs are:

| RFID PIN | ESP32 PIN |
| --- | --- |
| SCK | 18 |
| mosi | 19 |
| miso | 23 |
| rst | 4 |
| SDA (cs) | 5 |

Additionally I connected two LEDs to the ESP32 to show the status of the RFID reader:

| LED | PIN |
| --- | --- |
| green | 16 |
| red | 17 |

I cloned and adopted the [micropython-mfrc522](https://github.com/wendlers/micropython-mfrc522) to work with the ESP32.

## Twillio 

Nice post: https://www.twilio.com/en-us/blog/sms-doorbell-micropython-twilio

set the environment variables:
```

```
```
curl -X POST https://api.twilio.com/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json \
--data-urlencode "Body=Hi there" \
--data-urlencode "From=+15017122661" \
--data-urlencode "To=+15558675310" \
-u ACXXXXXXXXXXXXXXXXX:your_auth_token
```

## Deployment and Testing

See `just deploy` and `just test` for the deployment and testing.

