import numpy as np

f = lambda x, D, innerD, height : height/np.log(innerD/D)*np.log(x/innerD/2)
finv = lambda depth, D, innerD, height : np.exp(depth/height*np.log(D/innerD))*innerD/2

def circle_maker (file, D, T): #X is the x-position ,Y is the y-position, D is the diameter of the circle, T is the tool diameter
    O = D/2-T/2 #offset to the edge accounting for the dia of the tool
    
    file.write(f'G90\n')
    file.write(f'G1 Y{round(O, 6)} F30 \n',)
    file.write(f'G2 Y{round(-O, 6)} I0 J{round(-O, 6)} \n')
    file.write(f'Y{round(O, 6)} I0 J{round(O,6)}\n')
    file.write(f'G0 Y0\n')

def disk_maker(file, D, T):
    radius = 4/10*T
    while radius < D/2:
        circle_maker(file, 2*radius, T)
        radius += 9/10*T
    circle_maker(file, D, T)

def radius_setter(file, D, T, innerD, height, f, finv, cutting_depth):
    depth = height - cutting_depth
    radius = finv(depth, D, innerD, height)
    file.write('G20')
    if innerD < T or innerD >= 2: #Checking if we can make the smallest hole. later could change to be able to do for both
        return "Please choose a valid starting diameter."
    else:
        while radius > innerD/2:
            file.write('G91\n')
            file.write('G1 Z-0.1 F10\n')
            disk_maker(file, 2*radius,T)
            depth -= cutting_depth
            radius = finv(depth, D, innerD, height)

file = open("/Users/ketan/file.txt", "w")

radius_setter(file, 3, 0.25, 1, 3, f, finv, 0.05)
