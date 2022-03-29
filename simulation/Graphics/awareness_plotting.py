import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
X = [x for x in range(0, 10)]


def animate(i):
    data = open('../../awareness_data', 'r').read()
    if data != '':
        Y = [float(y) for y in np.array(data.split(' '))] 
        ax.clear()
        ax.bar(X, Y)
        

anim = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()