from pynput import keyboard
from squeezebox_controller import SqueezeBoxController
from time import sleep
from requests import get

controller = SqueezeBoxController("192.168.86.39", 9000)

def togglePlaying():
    info = controller._get_player_info('HiPi Study')
    if(info['mode'] == 'pause'):
        execute("PLAY")
    else:
        execute("PAUSE")

def volume(command):
    if(command == 'up'):
        execute("VOLUME UP")
    elif(command == 'down'):
        execute("VOLUME DOWN")
    elif(command == 'mute'):
        execute("MUTE")

def execute(command):
    params = {
      "player": "HiPi Study",
      "command": command
    }
    controller.simple_command(params)
    return

def shutdown():
    get('http://192.168.86.39/cgi-bin/main.cgi?ACTION=shutdown')
    
def on_press(key):
    try:
        key.char
    except AttributeError:
        if(key == keyboard.Key.media_play_pause):
            togglePlaying()
            sleep(0.5)
        elif(key == keyboard.Key.media_volume_up):
            volume('up')
            sleep(0.5)
        elif(key == keyboard.Key.media_volume_down):
            volume('down')
            sleep(0.5)
        elif(key == keyboard.Key.media_volume_mute):
            volume('mute')
            sleep(0.5)
        elif(key == keyboard.Key.media_next):
            execute("SKIP")
            sleep(0.5)
        elif(key == keyboard.Key.f10):
            shutdown()
            sleep(0.5)
        
def on_release(key):
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()