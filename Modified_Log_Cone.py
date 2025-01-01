import numpy as np

f = lambda x, D, innerD, height : height/np.log(innerD/D)*np.log(x/innerD/2)
finv = lambda depth, D, innerD, height : np.exp(depth/height*np.log(D/innerD))*innerD/2
def circle_maker (file, D, T): #X is the x-position ,Y is the y-position, D is the diameter of the circle, T is the tool diameter
    E = D/2-T/2 #offset to the edge accounting for the dia of the tool
    
    file.write(f'G90\n')
    file.write(f'G1 Y{round(E, 6)} F20 \n',)
    file.write(f'G2 Y{round(-E, 6)} I0 J{round(-E, 6)} \n')
    file.write(f'Y{round(E, 6)} I0 J{round(E,6)}\n')
    file.write(f'G0 Y0\n')

def disk_maker(file, D, T):
    j = D
    while j > T/2:
        circle_maker(file, j, T)
        j -= 9/10*T
    circle_maker(file, 3/2*T, T)

def radius_setter(file, D, T, innerD, height, f, finv, cutting_depth):
    depth = height - cutting_depth
    radius = finv(depth, D, innerD, height)
    if innerD < T or innerD >= 2: #Checking if we can make the smallest hole. later could change to be able to do for both
        return "Please choose a valid starting diameter."
    else:
        while radius > innerD/2:
            file.write('G91\n')
            file.write('G1 Z-0.1\n')
            disk_maker(file, 2*radius,T)
            depth -= cutting_depth
            radius = finv(depth, D, innerD, height)
file = open("/Users/ketan/file.txt", "w")
radius_setter(file, 3, 0.5, 1, 3, f, finv, 0.1)

