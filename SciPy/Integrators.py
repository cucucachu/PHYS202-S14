
import numpy as np;

def trapz(func, a, b, N):
    """Returns the numerical integration of the function func, from the limits a to b.
    This function uses the trapazoidal method to approximate the integral. It will use
    N slices, and becomes more accurate and more computationaly expensive as N increases.
    """
    h = (b - a) / N;
    k = np.arange(1, N);
    return h*(0.5*func(a) + 0.5*func(b) + func(a+k*h).sum());

def simps(func, a, b, N):
    """Returns the numerical integration of the function func, from the limits a to b.
    This function uses Simpson's method to approximate the integral. It will use
    N slices, and becomes more accurate and more computationaly expensive as N increases.
    """
    h = (b - a) / N;
    k1 = np.arange(1, N / 2 + 1);
    k2 = np.arange(1, N / 2);
    return (1./3.)*h*(func(a) + func(b) + 4.*func(a+(2*k1-1)*h).sum() + 2.*func(a+2*k2*h).sum());