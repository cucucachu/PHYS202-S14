import matplotlib.pyplot as plt;
import numpy as np;
from scipy.integrate import odeint;
import time as systime;
from matplotlib import animation
    
class Body:
    '''
    Body simulates a negligible mass body experiencing the gravity
    of a much larger object. 
    Instance variables:
        loc - a numpy array containing the trajectory and velocity of the Body.
        constant - The gravitational acceleration constant.
            format [x position, x velocity, y position, y velocity]
        
    '''
    
    def __init__(self, pos, vel, gamma, M, S, time):
        """
        Arguments:
            pos - An x y pair for the Body's initial position.
            vel - An x y pair for the Body's initial velocity.
            gamma - The gravitational constant.
            M - The ass of the galaxy center located at (0,0).
            S - The mass of this Body.
            time - a numpy array of time steps for the trajectory calculation.
        """
        try:
            self.loc = [pos[0], vel[0], pos[1], vel[1]];
            self.constant = -gamma * (M + S);
            
            self.trajectory(time);
        except:
            print "Body failed to initialize";
    
    def trajectory(self, time):
        """
        Calculates the trajectory of this object.
        Arguments:
            time - a numpy array of time steps for the trajectory calculation.
        """

        # function used by odeint which returns various derivitives
        def R(r, t):
            C = self.constant;
            xaccel = np.cos(np.arctan2(r[2], r[0])) * C / (r[0]**2 + r[2]**2);
            xvel = r[1];
            yaccel = np.sin(np.arctan2(r[2], r[0])) * C / (r[0]**2 + r[2]**2);
            yvel = r[3];

            return np.array([xvel, xaccel, yvel, yaccel])

        try:
            self.loc = odeint(R, self.loc, time);
        except:
            print "trajectory() failed.";
                
    def changeView(self, newX, newY):
        '''
        Converts all positions to change the origin of the graph
        Arguments:
            time - a numpy array of time steps for the trajectory calculation.
        '''
        
        self.loc[:,0] = self.loc[:,0] - newX;
        self.loc[:,2] = self.loc[:,2] - newY;

class Star(Body):
    '''
    Star calculates the trajectory of a negligible mass star due to the 
        gravitational effects of two galaxy centers.
    Instance Variables:
        loc - A numpy array with the trajectory and velocity information for
            star.
        gamma - The gravitational constant.
        M - The mass of the local galaxy center.
        S - The mass of the flyby galaxy.
    '''
        
    def __init__(self, radius, angle, sLoc, gamma, M, S, time, clockWise=False):
        """
        Arguments:
            radius, angle - The initial position of this star 
                in polar coordinates.
            sLoc - A four element array containing the initial conditions of the
                flyby galaxy.
            gamma - The gravitational constant.
            M - The ass of the galaxy center located at (0,0).
            S - The mass of this Body.
            time - a numpy array of time steps for the trajectory calculation.
            clockWise - a boolean determining the direction of spin.
        """        
        try:            
            x = radius * np.cos(angle);
            y = radius * np.sin(angle);
            accel = gamma * M;
            vel = np.sqrt(np.abs(accel / radius));
            vx = vel * np.cos(angle + np.pi/2.);
            vy = vel * np.sin(angle + np.pi/2.);
            
            if (clockWise == False):
                self.loc = [x, vx, y, vy, sLoc[0], sLoc[1], sLoc[2], sLoc[3]];
            else:
                self.loc = [x, -vx, y, -vy, sLoc[0], sLoc[1], sLoc[2], sLoc[3]];
            self.gamma = gamma;
            self.M = M;
            self.S = S;
            self.trajectory(time);
        except:
            print "Star failed to initialize";

    def trajectory(self, time):
        """
        Calculates the trajectory of this star.
        Arguments:
            time - a numpy array of time steps for the trajectory calculation.
        """

        # function used by odeint which returns various derivitives
        def R(r, t):
            gamma = self.gamma;
            M = self.M;
            S = self.S;
        
            C = -gamma * (M + S);
            
            xpos = r[0];
            xvel = r[1];
            ypos = r[2];
            yvel = r[3];
            Sxpos = r[4];
            Sxvel = r[5];
            Sypos = r[6];
            Syvel = r[7];
            rhoX = Sxpos - xpos;
            rhoY = Sypos - ypos;
            
            xaccel_term1 = (-gamma * M / (xpos**2 + ypos**2)) * np.cos(np.arctan2(ypos, xpos));
            yaccel_term1 = (-gamma * M / (xpos**2 + ypos**2)) * np.sin(np.arctan2(ypos, xpos));

            xaccel_term2 = (-gamma * S / (rhoX**2 + rhoY**2)) * np.cos(np.arctan2(rhoY, rhoX)); 
            yaccel_term2 = (-gamma * S / (rhoX**2 + rhoY**2)) * np.sin(np.arctan2(rhoY, rhoX)); 
            
            xaccel_term3 = (-gamma * S / (Sxpos**2 + Sypos**2)) * np.cos(np.arctan2(Sypos, Sxpos));
            yaccel_term3 = (-gamma * S / (Sxpos**2 + Sypos**2)) * np.sin(np.arctan2(Sypos, Sxpos));

            xaccel = xaccel_term1 - xaccel_term2 + xaccel_term3;
            yaccel = yaccel_term1 - yaccel_term2 + yaccel_term3;

            Sxaccel = np.cos(np.arctan2(r[6], r[4])) * C / (r[4]**2 + r[6]**2);
            Syaccel = np.sin(np.arctan2(r[6], r[4])) * C / (r[4]**2 + r[6]**2);

            return np.array([xvel, xaccel, yvel, yaccel,   \
                             Sxvel, Sxaccel, Syvel, Syaccel])

        try:
            self.loc = odeint(R, self.loc, time);        
        except:
            print "trajectory() failed.";

class Galaxy:
    '''
    Galaxy initializes a 2D interstellar system consisting of Stars and two
        galaxy centers. It can produce static images of the galaxies at points
        in time or produce an animation of the system.
    Instance Variables:
        gamma - The gravitational constant.
        M - The mass of the local galaxy center.
        S - The mass of the flyby galaxy.
        rings - A list of "rings" of stars. Each individual ring is a list
            of Star objects.
        S_Galaxy - An instance of Body representing the flyby galaxy.
        resolution - The amount of timeSteps between each unit in time.
        time - A numpy array of times for the trajectory calculations.
        xCoors, YCoors - Star Coordinates assembled into a single numpy array.
        gXs, gYs - Coordinates of the two galaxy centers collected in a single
            array for animation.
    '''
    
    def __init__(self, gamma, M, S):
        """
        Arguments:
            gamma - The gravitational constant.
            M - The ass of the galaxy center located at (0,0).
            S - The mass of this Body.
        """        
        self.gamma = gamma;
        self.M = M;
        self.S = S;
        self.rings = [];
        
    def setS(self, posx, posy, velx, vely):
        """
        Initializes the flyby galaxy.
        Arguments:
            posx, posy - the initial position for the galaxy.
            velx, vely - the initial velocity for the galaxy.
        """        
        self.S_Galaxy = Body((posx, posy), (velx, vely), self.gamma, self.M,\
                        self.S, self.time);
        
    def setTime(self, timeLimit, resolution):
        '''
        Sets up an np.array of the timespan to be passed to integrate.odeint
        Arguments
            timeLimit - The amount of time to simulate for.
            resolution - The amount of time steps per 1 unit of time to 
                calculate for.
        '''
        self.resolution = resolution;
        self.time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));
    
    def makeRing(self, radius, numStars, clockWise=False):
        '''
        Initializes a ring of stars.
        Requirements: setS must already have be called.
        Arguments:
            radius - The radial distance of the stars from galaxy center.
            numStars - The number of stars in this ring.
            clockWise - Boolean which determins the direction of spin
        '''
        ring = [];
        for i in range(numStars):
            angle = 2 * np.pi * i / numStars;
            ring.append(Star(radius, angle, self.S_Galaxy.loc[0], \
                             self.gamma, self.M, self.S, self.time, clockWise));
            
        self.rings.append(ring);
        
    def makeStars(self, rings, stars, clockWise=False):
        '''
        Initializes all of the stars in the galaxy.
        Requirements: setS must already have be called.
        Arguments:
            rings - The number of rings to make.
            numStars - The number of stars in each ring.
            clockWise - Boolean which determins the direction of spin
        '''
        for ring in range(1, rings+1):
            self.makeRing(ring*5, stars, clockWise);
            print "%2.1f%%" % (100 * float(ring) / float(rings));
            
    def makeToomreStars(self, clockWise=False):
        '''
        Initializes the galaxy to the specifications listed in the Toomre paper.
        Requirements: setS must already have be called.
        Arguments:
            clockWise - Boolean which determins the direction of spin
        '''
        curStar = 0.
        for ring in range(1, 6):
            for numStars in range(6 *(1 + ring)):
                self.makeRing((ring + 1) * 2.5, numStars, clockWise);
                curStar = curStar + 1;
                print "%2.1f%% finished" % (100. * float(curStar) / 120.);

            
    def changeView(self, newX, newY):
        '''
        Adjusts the ploting and animation perspective to a viewpoint.
        Requirements: All trajectories must already be calculated.
        Arguments:
            newX, newY = The point which will become the new origin.
        '''
        self.S_Galaxy.loc[:,0] = self.S_Galaxy.loc[:,0] - newX;
        self.S_Galaxy.loc[:,2] = self.S_Galaxy.loc[:,2] - newY;
        for ring in self.rings:
            for star in ring:
                star.changeView(newX, newY);
                
    def changeViewS(self):
        '''
        Adjusts the ploting and animation perspective to the viewpoint of 
            the flyby galaxy.
        Requirements: All trajectories must already be calculated.
        '''
        newX = self.S_Galaxy.loc[:,0];
        newY = self.S_Galaxy.loc[:,2];
        
        for ring in self.rings:
            for star in ring:
                star.changeView(newX, newY);
        
        self.S_Galaxy.loc[:,0] = -self.S_Galaxy.loc[:,0];
        self.S_Galaxy.loc[:,2] = -self.S_Galaxy.loc[:,2];
        
    def snapShot(self, time):
        '''
        Produces a plot of the system at time |time|
        Arguments:
            time - The time to draw the graph at.
        '''
        starXs = [];
        starYs = [];
        title = "Snapshot at time "+str(time);
        time = time*self.resolution;
        
        for ring in self.rings:
            for star in ring:
                starXs.append(star.loc[time, 0]);
                starYs.append(star.loc[time, 2]);
        
        plt.subplot(111, axisbg='black');
        
        plt.scatter(0, 0, c="yellow", s=100);                
        plt.scatter(starXs, starYs, c="white");
        plt.scatter(self.S_Galaxy.loc[time, 0], self.S_Galaxy.loc[time, 2], c="red", s=100);
        
        plt.title(title);
        plt.xlim(-100, 100);
        plt.ylim(-100, 100);
        plt.show();
        
        
    def timeLapse(self):
        '''
        Produces 5 plots of the system at equally spaced times.
        Requirments: Stars and Bodies have been initialized
        '''
        for i in np.linspace(0, int(max(self.time)), 5):
            self.snapShot(i);
            
    def animationSetup(self):
        '''
        Sets up xCoors and yCoors such that xCoors[time][star] will
            return the x coordinate of star |star| at time / resolution 
            |time|.
        Requirments:stars and bodies have been initialized
        '''
        self.xCoors = [];
        self.yCoors = [];
        self.gXs = [];
        self.gYs = [];
        
        for time in range(len(self.time)):
            instantXs = [];
            instantYs = [];
            instantGXs = [];
            instantGYs = [];
            for ring in self.rings:
                for star in ring:
                    instantXs.append(star.loc[time, 0]);
                    instantYs.append(star.loc[time, 2]);
            instantGXs.append(self.S_Galaxy.loc[time, 0]);
            instantGXs.append(0);
            instantGYs.append(self.S_Galaxy.loc[time, 2]);
            instantGYs.append(0);
            self.xCoors.append(instantXs);
            self.yCoors.append(instantYs);
            self.gXs.append(instantGXs);
            self.gYs.append(instantGYs);
        
    def animate(self, save=False, fileName="animation1.mp4"):
        '''
        Produces an optionally saves an animation of the system.
        Requirments: AnimationSetup() has already been called succesfully.
        Arguments:
            save - Whether or not the output should be saved.
            fileName - the address at which to save the file.
        '''
        fig = plt.figure()
        ax = plt.axes(xlim=(-100, 100), ylim=(-100, 100), axisbg="black");
        plt.title(fileName);
        
        stars, = ax.plot([], [], "w*", markersize=10);
        time_template = '+ %.3f Billion years';
        time_text = ax.text(.68, .05, '', transform=ax.transAxes, color="white");
        unit_text = ax.text(.73, .1, 'distance in kpc', transform=ax.transAxes,\
                             color="white");
        galaxies, = ax.plot([], [], "8", color="grey", markersize=10);

        def init():
            stars.set_data([], []);
            galaxies.set_data([], []);
            time_text.set_text('');
            return stars, galaxies, time_text;
            
        def animate(time):
            x = self.xCoors[time];
            y = self.yCoors[time];
            gXs = self.gXs[time];
            gYs = self.gYs[time];
            
            stars.set_data(x, y);
            galaxies.set_data(gXs, gYs);
            
            time_text.set_text(time_template%(self.time[time]));
            return stars, galaxies, time_text;
            
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(self.time), interval=33, blit=True);
        if (save == True):                               
            anim.save('animation1.mp4', fps=30, extra_args=['-vcodec', 'libx264']);
                                       
        plt.show();
