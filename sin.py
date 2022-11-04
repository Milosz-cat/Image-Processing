import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


M = 64
x = -32

fig, ax = plt.subplots()

x = np.linspace(0, 10, 500)
line, = ax.plot(x, np.sin(3 * x))


def animate(m):
    line.set_ydata(np.sin(3 * x + ((m * math.pi) / 10)))  # update the data.
    return line,


ani = animation.FuncAnimation(
    fig, animate, interval=40, blit=True, frames=range(-M // 2, M // 2))

plt.show()
