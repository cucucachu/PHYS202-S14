import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint

class Body:
    '''
    Body simulates a negligible mass body experiencing the gravity
    of a much larger object. 
    '''
    
    loc = [0, 0, 0, 0]
    # format [x velocity, x position, y velocity, y position]
   
    def __init__(self, pos, vel, constants):
        """
        @param pos - initial position (x, y)
        @param vel - initial velocity (x, y) """
        try:
            self.loc = [vel[0], pos[0], vel[1], pos[1]];
            self.constants = constants;
            self.FindConstant();
        except:
            print "Body failed to initialize";
    
    def __str__(self):
        return "location: " + str(self.loc);
    
    def Trajectory(self, timeLimit):
	     print "calulated trajectory";
		
		  # function used by odeint which returns various derivitives
	     def R(r, t):
            C = self.constant;
            xaccel = np.cos(np.arctan2(r[3], r[1])) * C / (r[1]**2 + r[3]**2)**.5);
				xvel = r[0];
            yaccel = np.sin(np.arctan2(r[3], r[1])) * C / (r[1]**2 + r[3]**2)**.5;
            yvel = r[2];

            return np.array([xaccel, xvel, yaccel, yvel])

        self.loc = odeint(R, loc, np.linspace(0, timeLimit, timeLimit + 1));
        

	 def FindConstant(self):
		  print "Finding Constant";
		  self.constant = -4;
	
	 def Plot(self):
		  x = self.loc[:,1]; #extracts the x values from loc
		  y = self.loc[:,3]; #extracts the y values from loc

	     plt.plot(x, y);
		  plt.scatter(0, 0, s=400, c = 'r')
		  plt.annotate("t = 0", xy = (x[0], loc[0,3]), xytext=(loc[0, 1] + 2, loc[0,3]- 15), \
						arrowprops=dict(facecolor='black', width=.5));
		  plt.grid();
		  plt.show();

body = Body([10, 5], [1, 1]);
print str(body)
body.trajectory();
