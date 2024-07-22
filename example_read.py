import mfrc522
import machine
import time

# red led and a green led
red = machine.Pin(14, machine.Pin.OUT)
green = machine.Pin(13, machine.Pin.OUT)


def card_detected(uid, card_type, data):
    print(uid, card_type, data)
    if uid == "0x73541514":
        card_rejected()
        print("Blocked card detected!")
        return
    green.on()
    time.sleep(2)
    green.off()


def card_rejected():
    red.on()
    time.sleep(2)
    red.off()


def main():
    card_reader = mfrc522.MFRC522(sck=18, mosi=19, miso=23, rst=4, cs=5)

    try:
        while True:

            (stat, tag_type) = card_reader.request(card_reader.REQIDL)

            if stat == card_reader.OK:

                (stat, raw_uid) = card_reader.anticoll()

                if stat == card_reader.OK:
                    print("New card detected")
                    card_type = tag_type
                    print("  - tag type: 0x%02x" % tag_type)
                    uid = f"0x%02x%02x%02x%02x" % (
                        raw_uid[0],
                        raw_uid[1],
                        raw_uid[2],
                        raw_uid[3],
                    )
                    print(
                        "  - uid	 : 0x%02x%02x%02x%02x"
                        % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    )
                    print("")

                    if card_reader.select_tag(raw_uid) == card_reader.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if (
                            card_reader.auth(card_reader.AUTHENT1A, 8, key, raw_uid)
                            == card_reader.OK
                        ):
                            data = card_reader.read(8)
                            print("Address 8 data: %s" % data)
                            card_reader.stop_crypto1()
                            card_detected(uid, card_type, data)
                        else:
                            print("Authentication error")
                            card_rejected()
                    else:
                        print("Failed to select tag")
                        card_rejected()

    except KeyboardInterrupt:
        print("Bye")
