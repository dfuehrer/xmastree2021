#!/usr/bin/env python3

# NOTE this relies on pandas, and matplotlib (and argparse)
import argparse
import sys


def main(coords=None, pattern=None, depthshade=True):
    coordsF = coords
    patternF = pattern
    # if no coords or pattern file given this cant run so exit
    if coordsF is None or patternF is None:
        print('Must give both a coordinates file and a pattern csv.')
        print(f'Try `{sys.argv[0]}` --help for more info')
        sys.exit(1)

    # import the big libraries
    # only done here so that it can exit quickly if the inputs are bad
    #import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.widgets as mwidgets

    # read in the coordinate and pattern data from the csvs
    coords: pd.DataFrame = pd.read_csv(coordsF, names=['x', 'y', 'z'])
    pattern: pd.DataFrame = pd.read_csv(patternF)

    # create a 3d figure
    #fig, ax = plt.subplots(subplot_kw={'projection':'3d'}, figsize=(10, 8), dpi=120)
    fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
    pattern /= 255
    #import time
    #ptime = time.thread_time()
    #pattern2 = pd.DataFrame({j: pattern[[f'R_{j}', f'G_{j}', f'B_{j}']].to_records(index=False).tolist() for j in range(len(pattern.columns) // 3)})
    pattern2 = pd.DataFrame(pattern[[f'R_{j}', f'G_{j}', f'B_{j}']].to_records(index=False).tolist() for j in range(len(pattern.columns) // 3)).T
    #print(time.thread_time() - ptime)
    # create a list of points for all the coords
    line = ax.scatter3D(coords['x'], coords['y'], coords['z'], '.', facecolor=pattern2.loc[0, :], edgecolor=None, depthshade=depthshade)

    size = coords['z'].max() - coords['z'].min()
    ax.set_xlim([-size/2, size/2])
    ax.set_ylim([-size/2, size/2])
    ax.set_zlim([0, size])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    persistant = {'i': 0}
    # this function pushes the colors to the next frame
    def animate_t():
        i = persistant['i']
        print(i)
        # change all the colors
        line.set_color(pattern2.loc[i, :])
        #if not i % 2:
        fig.canvas.draw_idle()
        persistant['i'] = i + 1 if i + 1 < pattern.shape[0] else 0
        return persistant['i']

    # create a timer to update the tree
    timer = fig.canvas.new_timer(interval=1)

    def animate(event):
        # clear callbacks and re-add it to be able to start it again
        timer.stop()
        timer.callbacks.clear()
        persistant['i'] = 0
        timer.add_callback(animate_t)
        timer.start()

    # create a button to animate the tree
    butax = fig.add_axes([.85, .1, .1, .03])
    but = mwidgets.Button(butax, 'Animate')
    # set the button to animate the tree when clicked
    but.on_clicked(animate)

    plt.show()


# parse the args
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--coords',  type=str, default=None, help='path to file of coordinates of the lights on the tree')
    parser.add_argument('-p', '--pattern', type=str, default=None, help='path to file of pattern    for the lights on the tree')
    parser.add_argument('-d', '--depthshade', action='store_true', help='flag to set whether to use shading to show depth')
    return parser.parse_args()

# do stuff
if __name__ == '__main__':
    args = parseArgs()
    main(**vars(args))
