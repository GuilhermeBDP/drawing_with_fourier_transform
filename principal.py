import pygame as pg
import math
import os
from dft_function import dft
import numpy as np
import matplotlib.image as mpimg
import pygame_widgets as pgw
import cv2

def epiCycles(x, y, fourier, rotation):
    for i in range(len(fourier)):
        freq = fourier[i][2]
        radius = fourier[i][3]
        phase = fourier[i][4]
        prevx = x
        prevy = y
        x += radius * math.cos(freq*time + phase + rotation)
        y += radius * math.sin(freq*time + phase + rotation)
        
        pg.draw.circle(screen, gray, (prevx+xo, prevy+yo), radius, 2)
        pg.draw.line(screen, black, (prevx+xo, prevy+yo), (x+xo, y+yo), 2)
        pg.draw.circle(screen, black, (x+xo, y+yo), 3)
        
    return [x, y]
    
imagem = cv2.imread('teste.jpg')
edge = cv2.Canny(imagem, 100, 200)

coord = []
for ym in range(0, edge.shape[0]):
    for xm in range(0, edge.shape[1]):
        if edge[ym, xm] != 0:
            coord = coord + [[xm, ym]]
coord = np.array(coord)

signalx = []
signaly = []

for i in range(len(coord)):
    val = 2 * coord[i][0]
    signalx.insert(len(signalx), val)
    
for i in range(len(coord)):
    val = 2 * coord[i][1]
    signaly.insert(len(signaly), val)

fourierX = dft(signalx)
fourierY = dft(signaly)

os.environ['SDL_VIDEO_CENTERED'] = '1'

#configuracao pygame
pg.init()
width, height = 800, 600
fps = 60
pg.display.set_caption("Fourier Series")
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

slider1 = pgw.Slider(screen, 100, 100, 200, 20, min = -800, max = 800, step = 1)
slider2 = pgw.Slider(screen, 100, 150, 200, 20, min = -600, max = 600, step = 1)

#cores
white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)
crimson = (230, 20, 32)
green = (0, 128, 0)

time = 0

xo = 200
yo = 300

offset = 150

path_list = []
    
run = True

while run:
    clock.tick(fps)
    screen.fill(white)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
    
    slider1.listen(events)
    slider1.draw()
    slider2.listen(events)
    slider2.draw()
    
    dx = slider1.getValue()
    dy = slider2.getValue()
    
    
    pathx = epiCycles(400, -200, fourierX, (0))
    pathy = epiCycles(-100, 100, fourierY, (math.pi/2))    
    pathxy = [pathx[0], pathy[1]]
    path_list.insert(0, pathxy)
    prevpx = 0
    prevpy = 0
    for i in range(len(path_list)):
        px = path_list[i][0]+xo+dx
        py = path_list[i][1]+yo+dy
        pg.draw.circle(screen, black, (px, py), 1)
        # if i != 0:
        #     pg.draw.line(screen, black, (px, py), (prevpx, prevpy), 2)
        prevpx = px
        prevpy = py
    
    pg.draw.line(screen, gray, (pathx[0]+xo, pathx[1]+yo), (pathxy[0]+xo+dx, pathxy[1]+yo+dy), 2)
    pg.draw.line(screen, gray, (pathy[0]+xo, pathy[1]+yo), (pathxy[0]+xo+dx, pathxy[1]+yo+dy), 2)
    if len(path_list) > 4000:
        path_list.pop()
    
    dt = 2 * math.pi / len(fourierY)
    time += dt
    pg.display.update()

pg.quit()

print('oi')
