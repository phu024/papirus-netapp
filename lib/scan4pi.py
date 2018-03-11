
#!/usr/bin/python
# Python code to print IP addresses and host name of local network
# to e-ink screen

import nmap
import sys
import socket
import smbus
import sys
import os
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
from papirus  import Papirus
from pexpect import pxssh
#import font1

epd = Papirus()
WHITE = 1
BLACK = 0
w = epd.width
h = epd.height
possible_fonts = [
'/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',            # R.Pi
'/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf',   # R.Pi
'/usr/share/fonts/truetype/freefont/FreeMono.ttf',                # R.Pi
]
FONT_FILE = ''
for f in possible_fonts:
    if os.path.exists(f):
        FONT_FILE = f
        break
    if '' == FONT_FILE:
        raise 'no font file found'

TEXT_FONT_SIZE1 = 11
TEXT_FONT_SIZE2 = 15
text_font1 = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE1)
text_font2 = ImageFont.truetype(FONT_FILE, TEXT_FONT_SIZE2)



def go(epd):
    display_running(epd)
    get_all_pi(epd)

# Code to show that a new speed test is running.
def display_running(epd):
    w = epd.width
    h = epd.height
    # initially set all white background
    image = Image.new('1', epd.size, WHITE)

    # prepare for drawing
    draw = ImageDraw.Draw(image)
    draw.rectangle((1, 1, w - 1, h - 1), fill=WHITE, outline=BLACK)
    draw.rectangle((2, 2, w - 2, h - 2), fill=WHITE, outline=BLACK)
    # text
    draw.text((10,35), "Looking for Raspberry Pi's", fill=BLACK, font=text_font2)
    draw.text((10,65), 'Please Wait.......', fill=BLACK, font=text_font2)
    # display image on the panel
    epd.display(image)
    epd.update()


def get_all_pi(epd):
        w = epd.width
        h = epd.height
        title="Found Pi's"
        r = 25
	subnet = '192.168.0.0/24' # Change to your Subnet if different
        # prepare for drawing
        image = Image.new('1', epd.size, WHITE)
        draw = ImageDraw.Draw(image)
        draw.rectangle((1, 1, w - 1, h - 1), fill=WHITE, outline=BLACK)
        draw.rectangle((2, 2, w - 2, h - 2), fill=WHITE, outline=BLACK)
        # text
        draw.text((5,5), title, fill=BLACK, font=text_font2)
        nm = nmap.PortScanner()

        nm.scan(subnet, arguments='-sP', sudo=True)
        for h in nm.all_hosts():
                if 'mac' in nm[h]['addresses']:
                        for x in nm[h]['vendor'].keys():
                                if x.startswith('B8:27:EB'): #Pi Lan Mac
                                        string = 'IP: ' + (nm[h]['addresses']['ipv4'])
                                        ipadd = (nm[h]['addresses']['ipv4'])
                                        draw.text((5,r), string, fill=BLACK, font=text_font1)
                                        try:
                                                s = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
                                                s.login(ipadd, 'pi','raspberry')
                                                s.logout()
                                                draw.text((125,r), 'Login Successfull', fill=BLACK, font=text_font1)
                                        except pxssh.ExceptionPxssh as e:
                                                draw.text((125,r), 'Login Failed', fill=BLACK, font=text_font1)
                                        r+=15
				if x.startswith('00:0F:13'): #known Wifi-Adaptor Mac
					string = 'IP: ' + (nm[h]['addresses']['ipv4'])
                                        ipadd = (nm[h]['addresses']['ipv4'])
                                        draw.text((5,r), string, fill=BLACK, font=text_font1)
                                        try:
                                                s = pxssh.pxssh(options={"StrictHostKeyChecking": "no","UserKnownHostsFile": "/dev/null"})
                                                s.login(ipadd, 'pi','raspberry')
                                                s.logout()
                                                draw.text((125,r), 'Login Successfull', fill=BLACK, font=text_font1)
                                        except pxssh.ExceptionPxssh as e:
                                                draw.text((125,r), 'Login Failed', fill=BLACK, font=text_font1)
                                        r+=15



        epd.display(image)
        epd.update()


def main():
        epd = Papirus()
        go(epd)                  
