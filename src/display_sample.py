from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

import numpy as np
from PIL import Image, ImageDraw

import Adafruit_SSD1306

IP = "127.0.0.1"
SERVER_PORT = 3001
CLIENT_PORT = 9008

#Parametros de sample
sample_values = []
sample_size = []
sample_width = 0
sample_height = 0

#---------------
EXTRA_LENGTH = 0
LINE_WIDTH = 2

#Parametros de oled
WIDTH = 128
HEIGHT = 64

#Inicializacion de oled
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

def pixel_handler(address, *value):

    if (address == "/sample/pos"):
        sample_values.append(value[0])
        
    if (address == "/sample/state"):
        if (value[0] == 1):
            sample_values.clear()
            print("STATE 1")

        elif(value[0] == 2):
            disp.clear()
            print("STATE 2")
            print(sample_size)

            sample_height = len(sample_values)
            PADDING = sample_height / 10
            
            image = Image.new(mode = "1", size = (sample_height + EXTRA_LENGTH, sample_height))
            draw = ImageDraw.Draw(image) 
            npval = np.array(sample_values)
            smpl_scaled = np.interp(npval, (npval.min(), npval.max()), (sample_height - PADDING, 0 + PADDING))

            for i in range(len(sample_values)-1):
                point_a = (i, int(smpl_scaled[i]))
                point_b = (i + 1, int(smpl_scaled[i+1]))
                draw.line((point_a, point_b), 1, LINE_WIDTH)

            # draw.line((len(smpl_scaled), 32, len(smpl_scaled)+EXTRA_LENGTH, 32), LINE_WIDTH)
            resized = image.resize((WIDTH, HEIGHT))
            bnw = resized.convert('1')
            # bnw.save(filename) 
            disp.image(bnw)  
            disp.display(bnw)

            sample_size.clear()
            draw.rectangle(((0, 0), WIDTH, HEIGHT), 0)
            
    if (address == "/sample/size"):
         sample_size.append(int(value[0]))
         print(address)

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

dispatcher = Dispatcher()
dispatcher.map("/sample*", pixel_handler)
dispatcher.set_default_handler(default_handler)

server = BlockingOSCUDPServer((IP, SERVER_PORT), dispatcher)
server.serve_forever()  # Blocks forever
