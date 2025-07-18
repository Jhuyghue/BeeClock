import pygame as pyg
import win32gui, win32api, win32con
import datetime
from math import pi, cos, sin
pyg.init()

#Creating the display
width = 296
height = 296
SCR = pyg.display.set_mode((width, height))
clock = pyg.time.Clock()
running = True

#Adding a title bar and icon
pyg.display.set_caption('BeeClock')
ico = pyg.image.load("assets/Icon.png").convert_alpha()
pyg.display.set_icon(ico)

#WIN32API to make a transparent background
hwnd = pyg.display.get_wm_info().get("window")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255,0,255), 0, win32con.LWA_COLORKEY)

#Making a list to add the clock sprites
clock_themes = [{
    "main": pyg.image.load('assets/MADO.png').convert_alpha(),
    "center": pyg.image.load('assets/MADO_C.png').convert_alpha(),
    "hour_hand": pyg.image.load('assets/MADO_HOUR.png').convert_alpha(),
    "minute_hand": pyg.image.load('assets/MADO_MIN.png').convert_alpha()
    },
    {"main": pyg.image.load('assets/PAST.png').convert_alpha(),
    "center": pyg.image.load('assets/PAST_C.png').convert_alpha(),
    "hour_hand": pyg.image.load('assets/PAST_HOUR.png').convert_alpha(),
    "minute_hand": pyg.image.load('assets/PAST_MIN.png').convert_alpha()
     },
    {"main": pyg.image.load('assets/MEL.png').convert_alpha(),
    "center": pyg.image.load('assets/MEL_C.png').convert_alpha(),
    "hour_hand": pyg.image.load('assets/MEL_HOUR.png').convert_alpha(),
    "minute_hand": pyg.image.load('assets/MEL_MIN.png').convert_alpha()}]

current_theme_index = 0 #Controlling the index of the theme
borderless = False #Keeping track if the border is on or not

#dimensions of a clock with a color variable and keeping track with the list
center = (width/2, height/2)
clock_radius = 158
WHITE = (255,255,255)

#Using Trig to find the polar coordinates to the cartesian
def polar_to_cart(r,theta):
    x = r * sin(pi * theta / 180)
    y = r * cos(pi * theta / 180)
    return x + width / 2,-(y - height / 2)

#Running a while loop and set to true to keep it running
while running:
    #Checking for any events
    for event in pyg.event.get():
        #Checking if any event is in queue. If the event type is quit,
        #then set the running boolean to false for exiting. True = doesn't exit.
        if event.type == pyg.QUIT:
            running = False

        #Right-click to switch themes
        elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 3:
            current_theme_index = (current_theme_index + 1) % len(clock_themes)

        #Spacebar to switch the frame
        elif event.type == pyg.KEYDOWN and event.key == pyg.K_SPACE:
            borderless = not borderless
            flags = pyg.NOFRAME if borderless else 0
            SCR = pyg.display.set_mode((width, height), flags)

    #Keeping the index of the themes
    theme = clock_themes[current_theme_index]

    # Using the datetime module to make the hands
    current_time = datetime.datetime.now()
    second = current_time.second
    minute = current_time.minute
    hour = current_time.hour

    #Code for the second hand
    sec_length = 120 #Length of the second hand
    sec_angle =  second * (360 / 60) #Speed/frames of the hand

    # Code for the MINUTE hand
    min_angle = (minute + second / 60) * (360 / 60)
    rotated_min = pyg.transform.rotozoom(theme["minute_hand"], -min_angle, 1)
    min_rect = rotated_min.get_rect(center=center)

    # Code for the HOUR hand
    hour_angle = (hour + minute / 60 + second / 3600) * (360 / 12)
    rotated_hour = pyg.transform.rotozoom(theme["hour_hand"], -hour_angle, 1)
    hour_rect = rotated_hour.get_rect(center=center)

    #Bliting the hands of the clock
    SCR.fill((255,0,255))
    SCR.blit(theme["main"], (0, 0))
    SCR.blit(rotated_hour, hour_rect)
    SCR.blit(rotated_min, min_rect)
    pyg.draw.line(SCR, WHITE, center, polar_to_cart(sec_length, sec_angle), 1)
    SCR.blit(theme["center"], (140,140))
    pyg.display.flip()
    clock.tick(60)

pyg.quit()