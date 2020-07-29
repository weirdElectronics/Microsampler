from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

from PIL import Image, ImageDraw

# import Adafruit_SSD1306

IP = "127.0.0.1"
SERVER_PORT = 3001

#Parametros de sample
sample_size = []

#---------------
FILENAME = "wavepic.png"
EXTRA_LENGTH = 0
LINE_WIDTH = 2

#Parametros de oled
WIDTH = 128
HEIGHT = 64
MIDDLE = HEIGHT/2

#Inicializacion de oled
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

def pointers(start_pos=0, end_pos=WIDTH):
    img = Image.open("output.png").convert('1')
    draw = ImageDraw.Draw(img)
    
    line_a = ((start_pos, 0), (start_pos, HEIGHT))
    line_b = ((end_pos, 0), (end_pos, HEIGHT))
    
    draw.line(line_a, 1)
    draw.line(line_b, 1)
    
    return img

def pixel_handler(address, *value):
        
    if (address == "/sample/state"):
        state = value[0]

        if (state == 0):
            pointer_a = int(value[1])
            pointer_b = int(value[2])
            
            disp.clear()
            print(pointer_a, pointer_b)
          #  print(f"""State 0: Not Recording
          #  - initial samplerate is -> {sample_size[0]}
          #  - final samplerate is -> {sample_size[1]}""")

            img = pointers(pointer_a, pointer_b)

            #draw = ImageDraw.Draw(img)
            
            disp.image(img)  
            disp.display(img)

            sample_size.clear()

        elif (state == 1):
            print("State 1: Recording!")

            
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
