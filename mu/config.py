
# TODO - this file should eventually read in config options from config files, either global or per-project.
# for now just edit the vars below as required

# board types: 'microbit', 'serial', 'webrepl'
board_type = 'serial'

serial_options = {
    'port': '/dev/cu.wchusbserial1410',
    'speed': 115200
}

webrepl_options ={
    'uri': 'ws://192.168.1.177:8266',
}



