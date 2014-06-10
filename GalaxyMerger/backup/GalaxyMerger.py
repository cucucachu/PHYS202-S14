import GalaxyMergerLib as GM;
import numpy as np;

# 1 time_unit = 1E8 years;
# 1 distance_unit = 1 kpc;
# 1 mass_unit = 1E10 Solar Masses;

gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
M = 25.; # units 1E10 Solar Masses
S = 100.; # units 1E10 Solar Masses
timeLimit = 10.; # 100 million years
resolution = 40;
time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

galaxy = GM.Galaxy(gamma, M, S);
print "Galaxy initialized...";
galaxy.setTime(timeLimit, resolution);
galaxy.setS(-30, 50, 27, 4);
print "Calculating trajectories...";
galaxy.makeStars(3, 3, True);
#galaxy.makeToomreStars();
#galaxy.changeViewS();
print "Galaxy trajectories calculated...";
print "Min distance:",min(np.sqrt(galaxy.S_Galaxy.loc[:,0]**2 + galaxy.S_Galaxy.loc[:,2]**2));
print "Working on animation...";
galaxy.animationSetup();
print "Animating...";
galaxy.animate();
