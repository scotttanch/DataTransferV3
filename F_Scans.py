from readgssi.dzt import readdzt
from readgssi.dzt import header_info
import numpy as np
import transfer_tools as tls
# import matplotlib as mpl
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import time
from scipy.signal import argrelextrema


# Function the returns the index of the element in the list that is closest to x 
def next_larget(vector:list,x:any):
    for element in vector:
        if element >= x:
            return vector.index(element)
        else:
            pass

def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        #ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    #ax.set_zlim3d([z - radius, z + radius])

folder = "D:\\Coding\\GPR_DATA\DZTs"

csvs = tls.full_stack(folder,'csv')
dzts = tls.full_stack(folder,'DZT')

X = []
Y = []
Z = []

f_xs = []
f_ys = []
f_zs = []
f_cs = []

for num in [0,1,2,3]:
    df = pd.read_csv(csvs[num])
    x_key = df.keys()[1]
    y_key = df.keys()[0]
    z_key = df.keys()[2]
    X = list(-1*df[x_key])
    Y = list(-1*df[y_key])
    Z = list(df[z_key])
    scan_number = dzts[num].split('_')[-1].split('.')[0]
    header,trace_array,_ = readdzt(dzts[num])
    #zeroing_row = np.where(trace_array == np.max(trace_array))[0][0]
    zeroing_row = 0
    num_samples = header['shape'][0]-header['timezero'][0]-zeroing_row
    num_traces = header['shape'][1]
    trace_array = trace_array[0]
    for i in range(0,zeroing_row):
        trace_array = np.delete(trace_array,i,0)

    distance = []
    cuml_dist = []
    for i in range(0,len(X)-1):
        xd = (X[i]-X[i+1])**2
        yd = (Y[i]-Y[i+1])**2
        zd = (Z[i]-Z[i+1])**2
        distance.append(np.sqrt(xd+yd+zd))
        cuml_dist.append(sum(distance))

    frac_along = []
    for j in range(len(cuml_dist)):
        frac_along.append(cuml_dist[j]/sum(distance))

    # Each point in the real sense path is some distance along the traveled path and therefore some percentage
    # of the way to the end of the path. Each trace in the dzt file is also some percentage from the end ie the
    # trace in the middle is 50% along the path. So we can find the percentage of the distance along the path
    # of each trace and then find its mapping along the path. will have to interpolate between realsense points
    f_x = []
    f_y = []
    f_z = [] # this is going to be zeros for now until i decide how deep each sample is
    f_c = []

    depth_planes = [10]
    min_val = -1*np.min(trace_array)
    trace_array = trace_array + min_val
    trace_array = (trace_array / np.max(trace_array))
    for i in range(num_traces):
        #for j in depth_planes:
        for j in range(num_samples):
            rel_per = i/num_traces
            if rel_per == 0:
                f_x.append(X[0])
                f_y.append(Y[0])
                f_z.append(-j)
                #color = [trace_array[j][i],trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                color = [trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                f_c.append(color)
            if rel_per == 1:
                f_x.append(X[1])
                f_y.append(Y[1])
                f_z.append(-j)
                #color = [trace_array[j][i],trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                color = [trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                f_c.append(color)
            else:                      
                next_index = next_larget(frac_along,rel_per)    
                interp_num = ((rel_per - frac_along[next_index-1])/(frac_along[next_index]-frac_along[next_index-1]))
                f_x.append(interp_num*(X[next_index] - X[next_index-1]) + X[next_index-1])
                f_y.append(interp_num*(Y[next_index] - Y[next_index-1]) + Y[next_index-1])
                f_z.append(-j)
                #color = [trace_array[j][i],trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                color = [trace_array[j][i],trace_array[j][i],trace_array[j][i]]
                f_c.append(color)

    f_xs.append(f_x)
    f_ys.append(f_y)
    f_zs.append(f_z)
    f_cs.append(f_c)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i in range(0,len(f_xs)):
        ax.scatter(f_xs[i],f_ys[i],f_zs[i],color=f_cs[i])
    ax.set_xlabel('X-Axis (ft)')
    ax.set_ylabel('Y-Axis (ft)')
    ax.set_zlabel('Z-Axis (Samples)')
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)
    plt.draw()
    plt.show()
    time.sleep(1)

# Plot a single Plane
#for i in range(0,len(f_xs)):
#    plt.scatter(f_xs[i],f_ys[i],color=f_cs[i])
#plt.show()

# Plot the whole field
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
#for i in range(0,len(f_xs)):
#    ax.scatter(f_xs[i],f_ys[i],f_zs[i],color=f_cs[i])
#ax.set_xlabel('X-Axis (ft)')
#ax.set_ylabel('Y-Axis (ft)')
#ax.set_zlabel('Z-Axis (Samples)')
#ax.set_box_aspect([1,1,1])
#set_axes_equal(ax)
#plt.show()