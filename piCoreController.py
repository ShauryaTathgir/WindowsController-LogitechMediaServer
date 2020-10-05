from pynput import keyboard
from squeezebox_controller import SqueezeBoxController
from time import sleep
from requests import get

controller = SqueezeBoxController(PLAYER_IP, PLAYER_PORT)

listen = True

def togglePlaying():
    info = controller._get_player_info(PLAYER_NAME)
    if(info['mode'] == 'pause'):
        execute("PLAY")
    else:
        execute("PAUSE")

def execute(command):
    params = {
      "player": PLAYER_NAME,
      "command": command
    }
    controller.simple_command(params)
    return

def shutdown():
    get('http://' + PLAYER_IP + '/cgi-bin/main.cgi?ACTION=shutdown')
    
def on_press(key):
    try:
        key.char
    except AttributeError:
        if(key == keyboard.Key.f9):
            listen = not listen
            sleep(0.5)
        elif(listen):
            if(key == keyboard.Key.media_play_pause):
                togglePlaying()
                sleep(0.5)
            elif(key == keyboard.Key.media_volume_up):
                execute("VOLUME UP")
                sleep(0.5)
            elif(key == keyboard.Key.media_volume_down):
                execute("VOLUME DOWN")
                sleep(0.5)
            elif(key == keyboard.Key.media_volume_mute):
                execute("MUTE")
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
