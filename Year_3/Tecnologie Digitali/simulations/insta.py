import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. initial render
x=np.linspace(0, 2*np.pi, 300)
fig, ax = plt.subplots()
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-1.2, 1.2)

# 2. update: shift the the arg of sin, using i
def update(i):
    line.set_ydata(np.sin(x-i*0.1))
    return line,

# 3. repeatedly calls update
# blit = don't redraw the canvas itself, just the line
ani = FuncAnimation(fig, update, frames=120, interval=33, blit=True)

plt.show()