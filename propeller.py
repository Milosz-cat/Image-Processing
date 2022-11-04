import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


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


# animation function.  This is called sequentially
def animate1(_m):
    x = np.linspace(0, 10, 500)
    y = np.sin(n * x + ((_m * math.pi) / 10))
    line.set_data(x, y)
    return line,


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig1, animate1, init_func=init1,
                               frames=m, interval=M, blit=True)


f = r"C:/Users/Miloszek/Desktop/VS_Code/Python/Signals/animation_5_480.gif" 
writergif = animation.PillowWriter(fps=60) #TUTAJ OPERUJESZ
anim.save(f, writer=writergif)

plt.show()


