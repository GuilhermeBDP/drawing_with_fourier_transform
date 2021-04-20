import pygame as pg
import pygame_widgets as pgw
import math
import os

os.chdir("C:\\Users\\guilh\\Google Drive\\Cursos Online\\Projetos Python\\Desenhando com Fourier")
os.environ['SDL_VIDEO_CENTERED'] = '1'
#configuracao pygame
pg.init()
width, height = 800, 600
fps = 60
pg.display.set_caption("Fourier Series")
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

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
wave_list = []

run = True

slider = pgw.Slider(screen, 100, 100, 200, 20, min = 1, max = 10, step = 1)
output = pgw.TextBox(screen, 500, 100, 50, 50, fontSize = 30)

while run:
    clock.tick(fps)
    screen.fill(white)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
            
    slider.listen(events)
    slider.draw()
    output.setText(slider.getValue())
    output.draw()
    
    iterations = slider.getValue()
    
    x = 0
    y = 0
    for i in range(iterations):
        prevx = x
        prevy = y
        n = i * 2 + 1
        radius = 70 * (4/(n*math.pi))
        x += radius * math.cos(n*time)
        y += radius * math.sin(n*time)
    
        pg.draw.circle(screen, gray, (prevx+xo, prevy+yo), radius, 2)
        pg.draw.line(screen, black, (prevx+xo, prevy+yo), (x+xo, y+yo), 2)
        pg.draw.circle(screen, black, (x+xo, y+yo), 1)
    
    wave_list.insert(0, y)
    prevpx = 0
    prevpy = 0
    for i in range(len(wave_list)):
        px = i+xo+offset
        py = wave_list[i]+yo
        pg.draw.circle(screen, black, (px, py), 1)
        if i != 0:
            pg.draw.line(screen, black, (px, py), (prevpx, prevpy), 2)
        prevpx = px
        prevpy = py
    pg.draw.line(screen, black, (x+xo, y+yo), (xo+offset, wave_list[0]+yo), 2)
    
    if len(wave_list) > 600:
        wave_list.pop()
    time += 0.05
    pg.display.update()

pg.quit()