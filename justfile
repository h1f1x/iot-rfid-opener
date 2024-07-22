SERIAL_PORT_NAME := "cu.SLAB_USBtoUART"

@help:
    just --list
    echo
    echo "SERIAL_PORT_NAME: {{SERIAL_PORT_NAME}}"

@init:
    -just _init_onetimer
    python -m venv venv
    echo "[>] Activate the virtual environment and add the micropython tools to the PATH:"
    echo "source venv/bin/activate"
    echo 'export PATH=$PATH:$(pwd)/micropython/tools/'
    echo 'alias mpremote="$(pwd)/micropython/tools/mpremote/mpremote.py"'
    echo 'pip install -r requirements.txt'

@_init_onetimer:
    echo "[>] Manually check your drivers. You find the URL in the README."
    git clone https://github.com/micropython/micropython.git
    git clone https://github.com/erikdelange/MicroPython-Logging
    git clone https://github.com/h1f1x/micropython-mfrc522

deploy:
    echo "[*] Deploying libs to the board ..."
    mpfshell -c "open {{SERIAL_PORT_NAME}}; lcd MicroPython-Logging; put logging.py " -n
    mpfshell -c "open {{SERIAL_PORT_NAME}}; lcd micropython-mfrc522; put mfrc522.py " -n
    echo "[*] Deploying application code ..."
    mpfshell -c "open {{SERIAL_PORT_NAME}}; put example_read.py; put example_led.py; put main.py; put config.json; ls" -n

alias test := run

# run the main.py script on the esp32
run:
    pyboard.py --device /dev/{{SERIAL_PORT_NAME}} -c 'import main; main.main()'

# run the example_led.py script on the esp32
debug:
    pyboard.py --device /dev/{{SERIAL_PORT_NAME}} -c 'import example_led; example_led.main()'

alias repl := remote

# opens a remote shell with micropython on the esp32
remote:
    mpfshell -c "open {{SERIAL_PORT_NAME}}; repl"

alias clean := erase_flash

# erase the flash of the esp32
erase_flash:
    echo "[*] Erasing the flash ..."
    esptool.py --chip esp32 --port /dev/{{SERIAL_PORT_NAME}} erase_flash

# flash micropython on the esp32
flash: 
    echo "[*] Flashing the firmware ..."
    esptool.py --chip esp32 --port /dev/{{SERIAL_PORT_NAME}} --baud 460800 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC-OTA-20240602-v1.23.0.bin

