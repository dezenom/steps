from numpy import loadtxt

def levels(level):
    LEVELS = loadtxt(f"res/levels/level{level}.csv",delimiter=",",dtype=int)
    return LEVELS
