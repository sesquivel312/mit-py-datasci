"""
"""
import argparse
import math

import matplotlib.pyplot as plt
import matplotlib.gridspec as gspec

from lib import sim_walks

p = argparse.ArgumentParser()
p.add_argument('--lengths', help='comma separated list of walk lengths')
p.add_argument('--num_walks', help='number of times to repeat walks for each length')
p.add_argument('--type', help='name of type of drunk to run through walks, affects how it chooses steps')
args = p.parse_args()

lengths = [int(e) for e in args.lengths.split(',')]
max_len = max(lengths)
nlengths = len(lengths)
nwalks = int(args.num_walks)

# todo verify input for drunk type
# todo is there a better, more secure way to convert the string to a class/instance
drunk_types = args.type.split(',')  # create list from string passed as CLI argument
ndrunks = len(drunk_types)  # number of different drunk types

# create an array of axes with one additional row
# the first row will contain the single plot with a line per dunk showing (walk_len, med_distance)
# the next row will contain a scatter plot for each walk length.  Each scatter plot will show the final
# positions of the drunks in each of the nwalk simulations, the marker type/color will differentiate the
# drunk types on each plot.
# B/c there is only one "mean distances" line plot (in the first row) the axes have to be created
# manually so that:
#   1) the "mean distance" plot has a better aspect ratio, and
#   2) the empty axes slots that would exist if a simple regular grid of axes were created via the subplots method
#      don't exist
# this requires use of the gridspec in order to specify where the various axes should exist on the grid
# and how much of the grid they should consume in the up/down and left/right directions.  I think this is
# something like the grid system that various CSS systems use (e.g. bootstrap)
fig = plt.figure(constrained_layout=True)
gs = gspec.GridSpec(nrows=2, ncols=nlengths, figure=fig)  # create the axes grid in/on the figure 2 rows by num lengths columns

markers = ['+', 'x', '1', '2', '3', '4', '.']  # markers used to represent points on a plot
colors = ['r', 'b', 'g', 'c', 'm', 'y']

for i, dt in enumerate(drunk_types):

    d = sim_walks(lengths, nwalks, dt)  # run the trials and collect the stats
    means = [d[k]['mean'] for k in range(len(d))]  # pick out the means for each walk length
    color = colors[i]  # color goes with drunk type

    a = fig.add_subplot(gs[0, 0:math.ceil(nlengths/2)])  # mean distance reached by walk len center of first row of axes grid (row #0)
    a.plot(lengths, means, color=color, label=dt)
    a.set_title('Mean dist from orig by walk len')
    a.grid(b=True)
    a.legend()
    a.set_xlabel('# steps taken')
    a.set_ylabel('mean dist in steps')
    # a.set_aspect(1.0)  # trying to make this look reasonable is a bit of a pain :(

    max_dist = 0
    for j, l in enumerate(lengths):
        # produce a scatter plot for each walk length

        curr_data = d[j]  # easier to type?
        positions = curr_data['positions']  # list of position objects containing a 2-tuple loc attribute (x,y)
        mean_dist = curr_data['mean']
        if curr_data['max'] > max_dist:
            max_dist = curr_data['max']
        # todo is there a better data model i seem to be creating new "things" to use data that's already there ...

        a = fig.add_subplot(gs[1, j:j+1])
        a.set_title(f'Final positions for walk length {l}')
        a.grid(b=True)
        a.set_xlim(xmin=-max_dist, xmax=max_dist)
        a.set_ylim(ymin=-max_dist, ymax=max_dist)
        # make charts consume equal distances on screen for equal # steps,
        # As there are multiple charts (axes) draw from lower left corner
        a.set_aspect(1.0, anchor='SW')  # square aspect ratio
        a.scatter(
            [p.loc[0] for p in positions],  # separate out the x & y positions into their own lists
            [p.loc[1] for p in positions],
            marker=markers[i],
            s=20,  # marker size
            color=color,
            label=f'{dt}, mean dist: {mean_dist}'
        )
        # the bbox... setting is some sort of ratio relative to the associated axis - I think
        # the two numbers are x & y, w/the traditional +/- orientation
        a.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3))
        a.set_xlabel('Steps E/W')
        a.set_ylabel('Steps N/S')

plt.show()

