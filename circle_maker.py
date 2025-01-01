import numpy as np

f = lambda x : np.log(x)

def circle_maker (file, D, T): #X is the x-position ,Y is the y-position, D is the diameter of the circle, T is the tool diameter
    E = D/2-T/2 #offset to the edge accounting for the dia of the tool
    file.write(f'G90')
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

def radius_setter(file, D, T, f, height, cutting_depth):
    #set log(T/2) as our starting z-depth
    offset = np.abs(np.log(T/2))
    new_height = height - offset

    depth = new_height-cutting_depth
    radius = np.exp(depth)

    while radius > T/2:
        file.write('G91\n')
        file.write('G1 Z-0.1')
        disk_maker(file, 2*radius,T)
        depth -= cutting_depth
        radius = np.exp(depth)
file = open("/Users/ketan/file.txt", "w")
radius_setter(file, 5, 0.5, f, 5, 0.1)