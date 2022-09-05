import time
import keyboard
from tkinter import Tk, Canvas
from objects import Object3d
from render import Render
from camera import Camera
from models import cube


root = Tk()
canvas = Canvas(root, width=600, height=400, bg='white')
canvas.pack()


cube1 = Object3d(model=cube, position=[200, 0, 200])
cube2 = Object3d(model=cube, position=[-200, 0, 1000])
cube3 = Object3d(model=cube, position=[200, 0, 1000])


camera = Camera(position=[0, 0, 0], angle=[0, 0, 0])
render = Render(objects=[cube1, cube2, cube3], camera=camera, canvas=canvas)


while True:
    if keyboard.is_pressed('esc'):
        break
    if keyboard.is_pressed('a'):
        camera.rotate_y(1)
    if keyboard.is_pressed('d'):
        camera.rotate_y(-1)

    if keyboard.is_pressed('w'):
        camera.rotate_x(1)
    if keyboard.is_pressed('s'):
        camera.rotate_x(-1)

    if keyboard.is_pressed('up'):
        camera.offset_z(10)
    if keyboard.is_pressed('down'):
        camera.offset_z(-10)

    cube1.rotate_x(0.1)
    cube1.rotate_y(0.1)
    cube1.rotate_z(0.1)

    render.render()
    root.update()
    time.sleep(1/60)
