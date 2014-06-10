import GalaxyMergerLib as GM;
import numpy as np;

# 1 time_unit = 1E8 years;
# 1 distance_unit = 1 kpc;
# 1 mass_unit = 1E10 Solar Masses;

def ToomreOne(save=False, filename="Animations/anim1.mp4"):
    '''Retrograde Passage. Equal mass bodies.'''
    
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-75, 55, 37, 0);
    
    print "Calculating trajectories...";
    
    #galaxy.makeStars(2,2);
    galaxy.makeToomreStars();
    
    print "Min distance:",min(np.sqrt(galaxy.S_Galaxy.loc[:,0]**2 \
                         + galaxy.S_Galaxy.loc[:,2]**2));
    print "Working on animation...";
    galaxy.animationSetup();
    print "Animating...";
    galaxy.animate(save, filename);

def ToomreTwo(save=False, filename="Animations/anim1.mp4"):
    '''Direct Passage. Equal mass bodies.'''
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # units 1 Billion years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-75, 55, 37, 0);
    
    print "Calculating trajectories...";
    #galaxy.makeStars(2, 2, True);
    galaxy.makeToomreStars(True);
    
    print "Min distance:",min(np.sqrt(galaxy.S_Galaxy.loc[:,0]**2 \
                         + galaxy.S_Galaxy.loc[:,2]**2));
    print "Working on animation...";
    galaxy.animationSetup();
    print "Animating...";
    galaxy.animate(save, filename);

def ToomreThree(save=False, filename="Animations/anim1.mp4"):
    '''Direct Passage. Flyby galaxy has 1/4 mass.'''
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 25.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-60, 55, 28.495, 0);
    
    print "Calculating trajectories...";
    #galaxy.makeStars(2, 2, True);
    galaxy.makeToomreStars(True);
    
    print "Min distance:",min(np.sqrt(galaxy.S_Galaxy.loc[:,0]**2 \
                         + galaxy.S_Galaxy.loc[:,2]**2));
    print "Working on animation...";
    galaxy.animationSetup();
    print "Animating...";
    galaxy.animate(save, filename);

def ToomreFour(save=False, filename="Animations/anim1.mp4"):
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 25.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-60, 55, 28.495, 0);
    
    print "Calculating trajectories...";
    
    #galaxy.makeStars(2, 2, True);
    galaxy.makeToomreStars(True);
    
    print "Min distance:",min(np.sqrt(galaxy.S_Galaxy.loc[:,0]**2 \
                         + galaxy.S_Galaxy.loc[:,2]**2));
    print "Working on animation...";
    galaxy.animationSetup();
    print "Animating...";
    galaxy.animate(save, filename);
    
def ToomreOneTimeLapse():
    '''Retrograde Passage. Equal mass bodies.'''
    
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-75, 55, 37, 0);
    
    print "Calculating trajectories...";
    
    #galaxy.makeStars(2,2);
    galaxy.makeToomreStars();
    
    galaxy.TimeLapse();

def ToomreTwoTimeLapse():
    '''Direct Passage. Equal mass bodies.'''
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # units 1 Billion years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-75, 55, 37, 0);
    
    print "Calculating trajectories...";
    galaxy.makeToomreStars(True);
    
    galaxy.timeLapse();

def ToomreThreeTimeLapse():
    '''Direct Passage. Flyby galaxy has 1/4 mass.'''
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 100.; # units 1E10 Solar Masses
    S = 25.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-60, 55, 28.495, 0);
    
    print "Calculating trajectories...";
    #galaxy.makeStars(2, 2, True);
    galaxy.makeToomreStars(True);
    
    galaxy.timeLapse();

def ToomreFourTimeLapse():
    gamma = 449.93; # units: kpc * m_unit * ( kpc / t_unit )^2;
    M = 25.; # units 1E10 Solar Masses
    S = 100.; # units 1E10 Solar Masses
    timeLimit = 10.; # 100 million years
    resolution = 40;
    time = np.linspace(0, timeLimit, resolution * (timeLimit + 1));

    print "Initializing Galaxy...";
    galaxy = GM.Galaxy(gamma, M, S);
    galaxy.setTime(timeLimit, resolution);
    galaxy.setS(-60, 55, 28.495, 0);
    
    print "Calculating trajectories...";
    
    #galaxy.makeStars(2, 2, True);
    galaxy.makeToomreStars(True);
    
    galaxy.timeLapse();
