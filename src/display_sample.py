from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

import numpy as np
from PIL import Image, ImageDraw

import Adafruit_SSD1306

IP = "127.0.0.1"
SERVER_PORT = 3001
CLIENT_PORT = 9008

WIDTH = 441000
HEIGHT = 64
EXTRA_LENGTH = 0
S_LINE_WIDTH = 2
PADDING = 5

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

y_list = []
sample_size = []
def pixel_handler(address, *value):

    if (address == "/sample/pos"):
        y_list.append(value[0])
        
    if (address == "/sample/state"):
        if (value[0] == 1):
            y_list.clear()
            
            print("STATE 1")
        elif(value[0] == 2):
            
            disp.clear()

            HEIGHT = len(y_list)
            PADDING = HEIGHT / 10
            image = Image.new(mode = "1", size = (len(y_list)+EXTRA_LENGTH, HEIGHT))
            draw = ImageDraw.Draw(image) 
            np_y = np.array(y_list)
            y_scaled = np.interp(np_y, (np_y.min(), np_y.max()), (HEIGHT - PADDING, 0 + PADDING))
            print("STATE 2")
            print(sample_size)

            for i in range(len(y_list)-1):
                y = int(y_scaled[i])
                y_2 = int(y_scaled[i+1])
                draw.line(((i, y),(i+1, y_2)), 1, S_LINE_WIDTH)

            # draw.line((len(y_scaled), 32, len(y_scaled)+EXTRA_LENGTH, 32), S_LINE_WIDTH)
            resized = image.resize((128, 64))
            resized.save("test_image.png")
            disp.display(resized)
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
