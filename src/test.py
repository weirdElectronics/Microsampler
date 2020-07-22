from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

#import numpy as np
from PIL import Image, ImageDraw

# import Adafruit_SSD1306

IP = "127.0.0.1"
SERVER_PORT = 3001
CLIENT_PORT = 9008

#Parametros de sample TODO eliminar datos inutilizados
sample_values = []
sample_size = []
sample_width = 0
sample_height = 0

#---------------
FILENAME = "wavepic.png"
EXTRA_LENGTH = 0
LINE_WIDTH = 2

#Parametros de oled
WIDTH = 128
HEIGHT = 64
MIDDLE = HEIGHT/2
# #Inicializacion de oled
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
# disp.begin()
# disp.clear()
# disp.display()

def pointers(start_pos=0, end_pos=WIDTH):
    img = Image.open("output.png").convert('1')
    draw = ImageDraw.Draw(img)
    
    point_a = ((start_pos, 0), (start_pos, HEIGHT))
    point_b = ((end_pos, 0), (end_pos, HEIGHT))
    

    draw.line(point_a, 1)
    draw.line(point_b, 1)
    
    return img


def pixel_handler(address, *value):
        
    if (address == "/sample/state"):
        state = value[0]

        if (state == 0):
            print("State 0: Not recording")

        elif (state == 1):
            print("State 1: Recording!")

        elif(state == 2):
            # disp.clear()
            print(f"""State 2: Read complete!
            - initial samplerate is -> {sample_size[0]}
            - final samplerate is -> {sample_size[1]}""")

            img = pointers(50, 70)

            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 0), (50, 50), 1)
            img.show()

            # disp.image(img)  
            # disp.display(img)

            sample_size.clear()
            
            
    if (address == "/sample/size"):
         val = int(value[0])
         sample_size.append(val)
         print(f"SAMPLERATE loaded in -> {address}, value: {val}")

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

dispatcher = Dispatcher()
dispatcher.map("/sample*", pixel_handler)
dispatcher.set_default_handler(default_handler)

server = BlockingOSCUDPServer((IP, SERVER_PORT), dispatcher)
server.serve_forever()  # Blocks forever
