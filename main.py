import network
import mfrc522
import machine
import time
import utime
import json
import ubinascii
import urequests
import logging

logging.basicConfig(level=logging.DEBUG)

# red led and a green led
red = machine.Pin(14, machine.Pin.OUT)
green = machine.Pin(13, machine.Pin.OUT)


def main():
    init()
    config = read_config()
    logging.debug("entering main loop ...")
    connect_wifi(config["ssid"], config["password"])
    card_reader = mfrc522.MFRC522(sck=18, mosi=19, miso=23, rst=4, cs=5)

    try:
        while True:
            do_card_scan(card_reader)
    except KeyboardInterrupt:
        logging.info("exiting main loop ...")


def init():
    logging.debug("initializing the board ...")
    red.off()
    green.off()


def read_config():
    filename = "config.json"
    logging.debug(f"reading config from  {filename} ...")
    with open(filename) as fp:
        return json.load(fp)


def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        logging.debug(f"Connecting to Wi-Fi [{ssid}] ...")
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            utime.sleep(1)
    logging.debug(f"Network config: {sta_if.ifconfig()}")


def do_card_scan(card_reader):
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


def card_detected(uid, card_type, data):
    print(uid, card_type, data)
    if uid != "0xa3cb4b36":
        card_rejected()
        return
    print(f"Access for {uid} granted.")
    green.on()
    time.sleep(2)
    green.off()


def card_rejected():
    red.on()
    time.sleep(2)
    red.off()


class TwilioSMS:
    base_url = "https://api.twilio.com/2010-04-01"

    def __init__(self, account_sid, auth_token):
        self.twilio_account_sid = account_sid
        self.twilio_auth = ubinascii.b2a_base64(
            "{sid}:{token}".format(sid=account_sid, token=auth_token)
        ).strip()

    def create(self, body, from_, to):
        data = "Body={body}&From={from_}&To={to}".format(
            body=body, from_=from_.replace("+", "%2B"), to=to.replace("+", "%2B")
        )
        r = urequests.post(
            "{base_url}/Accounts/{sid}/Messages.json".format(
                base_url=self.base_url, sid=self.twilio_account_sid
            ),
            data=data,
            headers={
                "Authorization": b"Basic " + self.twilio_auth,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        print("SMS sent with status code", r.status_code)
        print("Response: ", r.text)


if __name__ == "__main__":
    main()
