import sys, os

def _import(): 
    path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(path + "/../pysms")
    sys.path.append(path + "/../pygsm")
    

