import matplotlib.pyplot as plt;
import numpy as np;
from scipy.integrate import odeint;
import time as systime;
from matplotlib import animation

def circleInit(radius, angle, gamma, M):
    
    posx = radius * np.cos(angle);
    posy = radius * np.sin(angle);
    accel = gamma * M;
    vel = np.sqrt(np.abs(accel / radius));
    velx = vel * np.cos(angle + np.pi/2.);
    vely = vel * np.sin(angle + np.pi/2.);
    
    return [posx, velx, posy, vely];

def elipticalInit(a, angle, gamma, M):
    return;

def plotCircle(posx, velx, posy, vely, gamma, M):
    traj = [posx, velx, posy, vely];
    
    def R(r, t):
        xpos = r[0];
        xvel = r[1];
        ypos = r[2];
        yvel = r[3];
        
        xaccel = (-gamma * M / (xpos**2 + ypos**2)) * np.cos(np.arctan2(ypos, xpos));
        yaccel = (-gamma * M / (xpos**2 + ypos**2)) * np.sin(np.arctan2(ypos, xpos));
        
        return [xvel, xaccel, yvel, yaccel];
    
    traj = odeint(R, traj, np.linspace(0, 20, 4 * 20));
    plt.grid();
    plt.scatter(0, 0);
    plt.axis("equal");
    plt.plot(traj[:,0], traj[:,2]);
    
class Body:
    '''
    Body simulates a negligible mass body experiencing the gravity
    of a much larger object. 
    '''
    # format [x position, x velocity, y position, y velocity]
    
    def __init__(self, pos, vel, gamma, M, S, time):
        """
        @param pos - initial position (x, y)
        @param vel - initial velocity (x, y)
        """
        try:
            self.loc = [pos[0], vel[0], pos[1], vel[1]];
            self.constant = -gamma * (M + S);
            
            self.Trajectory(time);
        except:
            print "Body failed to initialize";
    
    def __str__(self):
        return "location:\n" + str(self.loc[:10]);
    
    def Trajectory(self, time):
        #print "Calulating trajectory";

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
            print "Trajectory() failed.";

    def Plot(self):
        x = self.loc[:,0]; #extracts the x values from loc
        y = self.loc[:,2]; #extracts the y values from loc

        plt.plot(x, y);
        plt.scatter(0, 0, s=400, c = 'r')
        plt.annotate("t = 0", xy = (x[0], y[0]), xytext=(x[0] + 2, y[0] - 15), \
            arrowprops=dict(facecolor='black', width=.5));
        plt.grid();
        plt.axis('equal');
        plt.show();
        
    def GetTrajectory(self):
        return self.loc[:,0], self.loc[:,2];
        
    def changeView(self, newX, newY):
        '''Converts all positions to change the origin of the graph'''
        
        self.loc[:,0] = self.loc[:,0] - newX;
        self.loc[:,2] = self.loc[:,2] - newY;

class Star(Body):
        
    def __init__(self, radius, angle, sLoc, gamma, M, S, time, clockWise=False):
        """
        @param radius - initial radius measured from local galaxy center
        @param angle - initial angle of this stars pos relative to galaxy center
        """
        
        try:
            x, vx, y, vy = circleInit(radius, angle, gamma, M);
            
            if (clockWise == False):
                self.loc = [x, vx, y, vy, sLoc[0], sLoc[1], sLoc[2], sLoc[3]];
            else:
                self.loc = [x, -vx, y, -vy, sLoc[0], sLoc[1], sLoc[2], sLoc[3]];
            self.gamma = gamma;
            self.M = M;
            self.S = S;
            self.Trajectory(time);
        except:
            print "Star failed to initialize";

    def Trajectory(self, time):
        #print "Calulating star trajectory";

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
            print "Trajectory() failed.";

    def Plot(self):
        x = self.loc[:,0]; #extracts the x values from loc
        y = self.loc[:,2]; #extracts the y values from loc
        Sx = self.loc[:,4];
        Sy = self.loc[:,6];

        plt.plot(x, y, label = 'This Star');
        plt.plot(Sx, Sy, "b*", label = 'Other Galaxy')
        
        plt.scatter(0, 0, s=400, c = 'r')
        
        plt.annotate("t = 0", xy = (x[0], y[0]), xytext=(x[0] + 2, y[0] - 15), \
            arrowprops=dict(facecolor='black', width=.5));
        
        plt.grid();
        plt.axis('equal');
        plt.xlim(-10, 10);
        plt.ylim(-10, 10);
        
        plt.legend(loc="best");
        plt.show();

class Galaxy:
    
    def __init__(self, gamma, M, S):
        self.gamma = gamma;
        self.M = M;
        self.S = S;
        self.rings = [];
        
    def setS(self, posx, posy, velx, vely):
        '''
           requirements: setTime must already have been called
           Sets up and calculates the trajectory of the other galaxy S
        '''
        self.S_Galaxy = Body((posx, posy), (velx, vely), self.gamma, self.M,\
                        self.S, self.time);
        
    def setTime(self, timeLimit, resolution):
        '''sets up the array of time for the ODE'''
        self.resolution = resolution;
        self.time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));
    
    def makeRing(self, radius, numStars, clockWise=False):
        '''requirements: setS must already have be called'''
        ring = [];
        for i in range(numStars):
            angle = 2 * np.pi * i / numStars;
            ring.append(Star(radius, angle, self.S_Galaxy.loc[0], \
                             self.gamma, self.M, self.S, self.time, clockWise));
            
        self.rings.append(ring);
        
    def makeRingEllipse(self, radius, numStars):
        '''Requirements: setS() must already have been called succesfully'''
        ring = [];
        for i in range(numStars):
            angle = 2 * np.pi * i / numStars;
        
    def makeStars(self, rings, stars, clockWise=False):
        '''requirements: setS must already have be called'''
        for ring in range(1, rings+1):
            self.makeRing(ring*5, stars, clockWise);
            print "%2.1f%%" % (100 * float(ring) / float(rings));
            
            
            
    def makeToomreStars(self, clockWise=False):
        '''requirements: setS must already have be called'''
        curStar = 0.
        for ring in range(1, 6):
            for numStars in range(6 *(1 + ring)):
                self.makeRing((ring + 1) * 2.5, numStars, clockWise);
                curStar = curStar + 1;
                print "%2.1f%% finished" % (100. * float(curStar) / 120.);

            
    def changeView(self, newX, newY):
        self.S_Galaxy.loc[:,0] = self.S_Galaxy.loc[:,0] - newX;
        self.S_Galaxy.loc[:,2] = self.S_Galaxy.loc[:,2] - newY;
        for ring in self.rings:
            for star in ring:
                star.changeView(newX, newY);
                
    def changeViewS(self):
        newX = self.S_Galaxy.loc[:,0];
        newY = self.S_Galaxy.loc[:,2];
        
        for ring in self.rings:
            for star in ring:
                star.changeView(newX, newY);
        
        self.S_Galaxy.loc[:,0] = -self.S_Galaxy.loc[:,0];
        self.S_Galaxy.loc[:,2] = -self.S_Galaxy.loc[:,2];
        
    def changeViewCOM(self):
        return;
        
    def snapShot(self, time):
        starXs = [];
        starYs = [];
        title = "Snapshot at time "+str(time);
        time = time*self.resolution;
        
        for ring in self.rings:
            for star in ring:
                starXs.append(star.loc[time, 0]);
                starYs.append(star.loc[time, 2]);
        
        #print "Star 1 distance from M", (self.rings[0][0].loc[time,0]**2 + self.rings[0][0].loc[time,2]**2)**.5
        
        #plt.figure(figsize=(400, 400)); #crashes for some reason
        plt.subplot(111, axisbg='black');
        
        plt.scatter(0, 0, c="yellow", s=100);                
        plt.scatter(starXs, starYs, c="white");
        plt.scatter(self.S_Galaxy.loc[time, 0], self.S_Galaxy.loc[time, 2], c="red", s=100);
        
        plt.title(title);
        plt.xlim(-20, 20);
        plt.ylim(-20, 20);
        plt.show();
        
        
    def timeLapse(self, timeLimit):
        '''Requires that stars and bodies have been initialized'''
        for i in range(0, int(timeLimit) + 1, 5):
            self.snapShot(i);
            
    def animationSetup(self):
        '''Requires that stars and bodies have been initialized
            Sets up xCoors and yCoors such that xCoors[time][star] will
            return the x coordinate of star <star> at time <time>'''
        self.xCoors = [];
        self.yCoors = [];
        
        for time in range(len(self.time)):
            instantXs = [];
            instantYs = [];
            for ring in self.rings:
                for star in ring:
                    instantXs.append(star.loc[time, 0]);
                    instantYs.append(star.loc[time, 2]);
            instantXs.append(self.S_Galaxy.loc[time, 0]);
            instantXs.append(0);
            instantYs.append(self.S_Galaxy.loc[time, 2]);
            instantYs.append(0);
            self.xCoors.append(instantXs);
            self.yCoors.append(instantYs);
        
    def animate(self):
        '''Requires that AnimationSettup has already been called succesfully'''
        fig = plt.figure()
        ax = plt.axes(xlim=(-100, 100), ylim=(-100, 100), axisbg="black");
        stars, = ax.plot([], [], "w*", markersize=10);
        #galaxies, = ax.plot([], [], "bo", markersize=100);
        #data.append(stars).

        def init():
            stars.set_data([], []);
            return stars,
            
        def animate(time):
            x = self.xCoors[time];
            y = self.yCoors[time];
            stars.set_data(x, y);
            return stars,

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=len(self.time), interval=33, blit=True);
                                       
        anim.save('animation1.mp4', fps=30, extra_args=['-vcodec', 'libx264']);
                                       
        plt.show();
