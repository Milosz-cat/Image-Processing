import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import math
from PIL import Image, ImageSequence

def make_animation():
    # First set up the figure, the axis, and the plot element we want to animate
    fig1 = plt.figure()
    ax = plt.axes(projection='polar')
    line, = ax.plot([], [], lw=3, color='black')


    # initialization function: plot the background of each frame
    def init1():
        line.set_data([], [])
        return line,


    n = 5  #ilosc łopatek ,dla n=3 -> m=30,dla n=5 -> m=0
    M = 64 
    m = range(-30,451) #TUTAJ OPERUJESZ(-M // 2, M // 2 + 1) przy tym zacina się, (-30,61),(-30,211)
    # w  tym range uzyskujemy 480 klatek dzięki czemu mamy duże możliwości w zmienianiu predkości sensora

    # animation function.  This is called sequentially
    def animate1(_m):
        x = np.linspace(0, 10, 500)
        y = np.sin(n * x + ((_m * math.pi) / 10))
        line.set_data(x, y)
        return line,


    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig1, animate1, init_func=init1,
                                frames=m, interval=M, blit=True)


    writer = PillowWriter(fps=30)
    anim.save(f'animation_{n}_{m[-1] - m[0]}.gif', writer=writer)
    

def rollingshutter():
    image_old = 'animation_5_480.gif' #choose animation
    im = Image.open(image_old)

    i = 0
    width = 640
    height = 480
    j = 2 # height/frames , with j we change speed of sensor , higher j ==> higher speed of sensor

    ims = []
    frames = []

    for i, frame in enumerate(ImageSequence.Iterator(im)):  #saving frames and rows (1st row from 1st frame,2nd row from 2nd frame etc.)
        ims.append(im.crop((0, i*j, width, i*j+j)))
        frames.append(frame.crop((0, 0, width, height)))
        if i == height//j:  #if we want to slow down sensor
            break



    for k, item in enumerate(frames):
        for n in range(k):
            item.paste(ims[n], (0, n*j)) #pasting each row to frame

        
        
    frames[0].save(f'rolling_shutter_5_480_{j}.gif', #creating gif from new frames
                save_all=True, append_images=frames[1:], optimize=False, duration=40, loop=0)

if __name__ == '__main__':
    make_animation()
    rollingshutter()