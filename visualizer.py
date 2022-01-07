#!/usr/bin/env python3

# NOTE this relies on pandas, and matplotlib (and argparse)
import argparse
import sys


def main(coords=None, pattern=None):
    # if no coords or pattern file given this cant run so exit
    if coords is None or pattern is None:
        print('Must give both a coordinates file and a pattern csv.')
        print(f'Try `{sys.argv[0]}` --help for more info')
        sys.exit(1)

    # import the big libraries
    # only done here so that it can exit quickly if the inputs are bad
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.widgets as mwidgets

    # read in the coordinate and pattern data from the csvs
    coords = pd.read_csv(coords, names=['x', 'y', 'z'])
    pattern = pd.read_csv(pattern)

    # create a 3d figure
    fig, ax = plt.subplots(subplot_kw={'projection':'3d'}, figsize=(10, 8), dpi=120)
    # create a list of points for all the coords
    lines = [ax.plot(coords['x'][i], coords['y'][i], coords['z'][i], '.')[0] for i in coords.index]

    # this function pushes the colors to the next frame
    def animate_t(persistant={'i':0}):
        i = persistant['i']
        print(i)
        # change all the colors in a loop
        for j, line in enumerate(lines):
            color = (pattern[f'R_{j}'][i]/255, pattern[f'G_{j}'][i]/255, pattern[f'B_{j}'][i]/255)
            line.set_color(color)
        fig.canvas.draw()
        persistant['i'] = i + 1 if i + 1 < pattern.shape[0] else 0
        return persistant['i']

    # create a timer to update the tree
    timer = fig.canvas.new_timer(interval=25, callbacks=[(animate_t, (), {})])

    def animate(event):
        print(event)
        timer.start()

    # create a button to animate the tree
    butax = fig.add_axes([.85, .1, .1, .03])
    but = mwidgets.Button(butax, 'animate')
    # set the button to animate the tree when clicked
    but.on_clicked(animate)

    plt.show()


# parse the args
def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--coords',  type=str, default=None, help='path to file of coordinates of the lights on the tree')
    parser.add_argument('-p', '--pattern', type=str, default=None, help='path to file of pattern    for the lights on the tree')
    return parser.parse_args()

# do stuff
if __name__ == '__main__':
    args = parseArgs()
    main(**vars(args))
