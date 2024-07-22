SERIAL_PORT_NAME := "cu.SLAB_USBtoUART"

@help:
    just --list
    echo
    echo "SERIAL_PORT_NAME: {{SERIAL_PORT_NAME}}"

init:
    echo "[] Manually check your drivers. You find the URL in the README."
    git clone https://github.com/micropython/micropython.git
    git clone https://github.com/erikdelange/MicroPython-Logging
    echo "[ ] Activate the virtual environment and add the micropython tools to the PATH:"
    echo "source venv/bin/activate"
    echo 'export PATH=$PATH:$(pwd)/micropython/tools/'
    echo 'alias mpremote="$(pwd)/micropython/tools/mpremote/mpremote.py"'


deploy:
    mpfshell -c "open {{SERIAL_PORT_NAME}}; put example_read.py; put example_led.py; put main.py; ls" -n

alias test := run

run:
    pyboard.py --device /dev/{{SERIAL_PORT_NAME}} -c 'import main; main.main()'

debug:
    pyboard.py --device /dev/{{SERIAL_PORT_NAME}}-c 'import example_led; example_led.main()'

alias repl := remote

remote:
    mpfshell -c "open {{SERIAL_PORT_NAME}}; repl"