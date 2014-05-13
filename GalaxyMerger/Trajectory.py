#@author: Cody Jones
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint

C = -4 # a constant which is a combo of the grav const, masses, etc.
timeLimit = 99

# format [x velocity, x position, y velocity, y position]
loc = [1, 10, 2, 5] # initial values


# function used by odeint which returns various derivitives
def R(r, t):
    xaccel = np.cos(np.arctan2(r[3], r[1])) * (C / (r[1]**2 + r[3]**2)**.5); 
    xvel = r[0];
    yaccel = np.sin(np.arctan2(r[3], r[1])) * C / (r[1]**2 + r[3]**2)**.5;
    yvel = r[2];
    
    return np.array([xaccel, xvel, yaccel, yvel])


loc = odeint(R, loc, np.linspace(0, timeLimit, timeLimit + 1));
    
x = loc[:,1]; # extracts the x values from loc
y = loc[:,3]; # extracts the y values from loc

plt.plot(x, y);
plt.scatter(0, 0, s=400, c = 'r')
plt.annotate("t = 0", xy = (x[0], loc[0,3]), xytext=(loc[0, 1] + 2, loc[0,3]- 15), \
            arrowprops=dict(facecolor='black', width=.5));

plt.grid();
plt.show();