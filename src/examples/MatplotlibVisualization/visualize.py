import dateutil.parser
import matplotlib.pyplot as plt
import numpy as np

marker_style = dict(linestyle='', color='0.8', markersize=10, mfc="C0", mec="C0")
                    
# Data for plotting
data = np.genfromtxt("data.txt", delimiter=',', dtype=None)
features = np.genfromtxt("res.txt", delimiter=',', dtype=None)

fig, ax = plt.subplots()
ax.plot(range(0, len(data)), data)

ax.plot(features, data[features], marker='.', **marker_style)

ax.set(xlabel='data index', ylabel='data value')
ax.grid()

fig.savefig("MatplotlibVisRes.png")
plt.show()
