import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve
from scipy import interpolate
import argparse

# Debug Settings
# np.set_printoptions(linewidth=250)

def get_summed_distance(x, y):
    dist = 0
    for i in range(1, len(x)):
        dist += np.sqrt((x[i]-x[i-1])**2 + (y[i]-y[i-1])**2)
    return dist

def get_ctrl_pts(input_file):
    x = []
    y = []
    with open(input_file, 'r') as f:
        for line in f:
            val = line.split()
            x.append(float(val[0]))
            y.append(float(val[1]))
    t = [0]
    for j in range(1, len(x)-1):
        t.append(get_summed_distance(x[:j+1], y[:j+1])/get_summed_distance(x, y))
    t.append(1)
    knots=np.append([0,0,0],t)
    knots=np.append(knots,[1,1,1])
    n_matrix = np.zeros((len(x)+2, len(x)+2))
    d_matrix_x = np.zeros((len(x)+2))
    d_matrix_y = np.zeros((len(y)+2))
    for i in range(len(x)):
        for j in range(len(x)+2):
            n = None
            if j+3 < len(knots) and t[i] >= knots[j] and t[i] < knots[j+1]:
                n = ((t[i]-knots[j])**3)/((knots[j+1] - knots[j])*(knots[j+2]-knots[j])*(knots[j+3]-knots[j]))

            elif j+4 < len(knots) and t[i] >= knots[j+1] and t[i] < knots[j+2]:
                n = ((t[i]-knots[j])**2*(knots[j+2]-t[i]))/((knots[j+2]-knots[j+1])*(knots[j+3]-knots[j])*(knots[j+2]-knots[j])) + ((knots[j+3]-t[i])*(t[i]-knots[j])*(t[i]-knots[j+1]))/((knots[j+2]-knots[j+1])*(knots[j+3]-knots[j+1])*(knots[j+3]-knots[j])) + ((knots[j+4]-t[i])*(t[i]-knots[j+1])**2)/((knots[j+2]-knots[j+1])*(knots[j+4]-knots[j+1])*(knots[j+3]-knots[j+1]))

            elif j+4 < len(knots) and t[i] >= knots[j+2] and t[i] < knots[j+3]:
                n = ((t[i]-knots[j])*(knots[j+3]-t[i])**2)/((knots[j+3]-knots[j+2])*(knots[j+3]-knots[j+1])*(knots[j+3]-knots[j])) + ((knots[j+4]-t[i])*(knots[j+3]-t[i])*(t[i]-knots[j+1]))/((knots[j+3]-knots[j+2])*(knots[j+4]-knots[j+1])*(knots[j+3]-knots[j+1])) + ((knots[j+4]-t[i])**2*(t[i]-knots[j+2]))/((knots[j+3]-knots[j+2])*(knots[j+4]-knots[j+2])*(knots[j+4]-knots[j+1]))
                
            elif j+4 < len(knots) and t[i] >= knots[j+3] and t[i] < knots[j+4]:
                n = ((knots[j+4]-t[i])**3)/((knots[j+4]-knots[j+3])*(knots[j+4]-knots[j+2])*(knots[j+4]-knots[j+1]))
                
            if n:
                n_matrix[i+1][j] = n

    n_matrix[0][0] = 1
    n_matrix[n_matrix.shape[0]-1][n_matrix.shape[1]-1] = 1
    n = len(x)-1

    n_matrix[1][0] = 6*(knots[4]-t[0])/((knots[4]-knots[3])*(knots[4]-knots[2])*(knots[4]-knots[1]))
    n_matrix[-2][-3] = (2*(t[-1]-knots[n])-4*(knots[n+3]-t[-1]))/((knots[n+3]-knots[n+2])*(knots[n+3]-knots[n+1])*(knots[n+3]-knots[n])) + (-2*(knots[n+4]-t[-1])-2*(knots[n+3]-t[-1])+2*(t[-1]-knots[n+1]))/((knots[n+3]-knots[n+2])*(knots[n+4]-knots[n+1])*(knots[n+3]-knots[n+1])) + (4*(knots[n+4]-t[-1])-2*(t[-1]-knots[n+2]))/((knots[n+4]-knots[n+2])*(knots[n+4]-knots[n+2])*(knots[n+4]-knots[n+1]))

    n_matrix[1][1] = (2*(t[0]-knots[1])-4*(knots[4]-t[0]))/((knots[4]-knots[3])*(knots[4]-knots[2])*(knots[4]-knots[1])) + (-2*(knots[5]-t[0])-2*(knots[4]-t[0])+2*(t[0]-knots[2]))/((knots[4]-knots[3])*(knots[5]-knots[2])*(knots[4]-knots[2])) + (4*(knots[5]-t[0])-2*(t[0]-knots[3]))/((knots[4]-knots[3])*(knots[5]-knots[3])*(knots[5]-knots[2]))
    n_matrix[-2][-2] = (-2*(knots[n+3]-t[-1]))/((knots[n+4]-knots[n+2])*(knots[n+4]-knots[n+1])*(knots[n+3]-knots[n+1])) + (2*(knots[n+4]-t[-1])-2*(t[-1]-knots[n+1])-2*(t[-1]-knots[n+2]))/((knots[n+3]-knots[n+2])*(knots[n+4]-knots[n+2])*(knots[n+4]-knots[n+1])) + (2*(knots[n+5]-t[-1])-4*(t[-1]-knots[n+2]))/((knots[n+3]-knots[n+2])*(knots[n+5]-knots[n+2])*(knots[n+5]-knots[n+2]))

    n_matrix[1][2] = (-2*(knots[4]-t[0]))/((knots[4]-knots[3])*(knots[5]-knots[2])*(knots[4]-knots[2])) + (2*(knots[5]-t[0])-2*(t[0]-knots[2])-2*(t[0]-knots[3]))/((knots[4]-knots[3])*(knots[5]-knots[3])*(knots[5]-knots[2])) + (2*(knots[6]-t[0])-4*(t[0]-knots[3]))/((knots[4]-knots[3])*(knots[6]-knots[3])*(knots[5]-knots[3]))
    n_matrix[-2][-1] = (6*(t[n]-knots[n+2]))/((knots[n+3] - knots[n+2])*(knots[n+3]-knots[n+2])*(knots[n+5]-knots[n+2]))
                
    for i in range(len(x)):
        if i == 0:
            d_matrix_x[i] = x[i]
            d_matrix_y[i] = y[i]
        elif i == n:
            d_matrix_x[i+2] = x[i]
            d_matrix_y[i+2] = y[i]
        else:
            d_matrix_x[i+1] = x[i]
            d_matrix_y[i+1] = y[i]
    
    ctrl_pt_x = solve(n_matrix, d_matrix_x)
    ctrl_pt_y = solve(n_matrix, d_matrix_y)

    return ctrl_pt_x, ctrl_pt_y, knots, x, y
    
def plot_bspline(ctrl_pt_x, ctrl_pt_y, knots, num_points=50, x=None, y=None, degree=3):
    tck=[knots,[ctrl_pt_x,ctrl_pt_y],degree]
    steps=np.linspace(0,1,num_points,endpoint=True)
    out = interpolate.splev(steps,tck) 

    plt.plot(ctrl_pt_x,ctrl_pt_y,'k--',label='Control polygon',marker='o',markerfacecolor='red')
    if x and y:
        plt.scatter(x,y, label='Coordinates',marker='o', color='blue')
    plt.plot(out[0],out[1],'b',linewidth=2.0,label='B-spline curve')
    plt.legend(loc='best')
    plt.title('Cubic B-spline curve')
    plt.show()

def write_output(output_filename, ctrl_pt_x, ctrl_pt_y, knots):
    degree = 3
    cnt_num = len(ctrl_pt_x)
    knots = [str(x) for x in knots]
    with open(output_filename, 'w') as f:
        f.write(f'{degree}\n')
        f.write(f'{cnt_num}\n')
        f.write(' '.join(knots)+'\n')
        for i in range(cnt_num):
            if i != cnt_num-1:
                f.write(f'{ctrl_pt_x[i]} {ctrl_pt_y[i]}\n')
            else:
                f.write(f'{ctrl_pt_x[i]} {ctrl_pt_y[i]}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='B-Spline Interpolation')
    parser.add_argument('inputfile', help='Path to input file')
    parser.add_argument('outputfile', help='Path to save output file')
    parser.add_argument('--steps', type=int, default=50, help='Number of steps to draw curve')
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()
    FILENAME = args.inputfile
    OUTPUT = args.outputfile
    NUM_POINTS = args.steps
    ctrl_pt_x, ctrl_pt_y, knots, x, y = get_ctrl_pts(FILENAME)
    if args.plot:
        plot_bspline(ctrl_pt_x, ctrl_pt_y, knots, NUM_POINTS, x, y)
    write_output(OUTPUT, ctrl_pt_x, ctrl_pt_y, knots)