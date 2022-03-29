import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)



def animate(i):
    data = open('../../population_size_data', 'r').read()
    if data != '':
        Y = [float(y) for y in np.array(data.split(','))[:-1]]
        X = [x for x in range(0, len(Y))]
        ax.clear()
        ax.plot(X, Y)
        

anim = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()