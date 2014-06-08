import GalaxyMergerLib as GM;
import numpy as np;

gamma = 25.;
M = 10.;
S = 100.;
timeLimit = 100.;
resolution = 4;
time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

galaxy = GM.Galaxy(gamma, M, S);
print "Galaxy initialized...";
galaxy.setTime(timeLimit, resolution);
galaxy.setS(10, 25, 1, -3);
galaxy.makeStars(3, 3);
print "Galaxy trajectories calculated...";
print "Working on animation...";
galaxy.animationSetup();
print "Animating...";
galaxy.animate();
