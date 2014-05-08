
def fourPtCenteredDiff(x, y):
    """Returns an array containing the the derivitive of y with respect to x
    using a four point centered method."""
    dydx = np.zeros(y.shape, float);
    dydx[2:-3] = (y[:-5] - 8 * y[1:-4] + 8 * y[3:-2] - y[4:-1]) \
    / (x[:-5] - 8 * x[1:-4] + 8 * x[3:-2] - x[4:-1])
    dydx[1] = (y[2] - y[0]) / (x[2] / x[0]);
    dydx[-2] = (y[-1] - y[-3]) / (x[-1] - x[-3]);
    dydx[0] = (y[1] - y[0]) / (x[1] - x[0]);
    dydx[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2]);
    return dydx;

def twoPtForwardDiff(x, y):
    """Returns an array containing the forward diff of y with respect to x"""
    dydx = np.zeros(y.shape,float);
    dydx[0:-1] = np.diff(y)/np.diff(x);
    dydx[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2]);
    return dydx;

def twoPtCenteredDiff(x, y):
    """Returns an array containing the differentiation of y with respect to x,
    using a centered difference"""
    dydx = np.zeros(y.shape,float);
    dydx[1:-1] = (y[2:] - y[:-2]) / (x[2:] - x[:-2]);
    dydx[0] = (y[1] - y[0]) / (x[1] - x[0]);
    dydx[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2]);
    return dydx;