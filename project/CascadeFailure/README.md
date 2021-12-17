# Cascade Failure


## Contents
* cf_data:  contains the results of our Cascade Failure model
* data: contains gml and graphml data for the network used.
* plots_and_images: contains all plots used in the Cascade Failure part of the paper and presentation
* average_avalanche_size.py: Program to create the average avalanche plot
* cascade_visualisation.py: Program to visualize one Cascade Failure. Creates an image for each time step which then could be used to create a .gif
* cf_betweenness_parallell.py: Applies the Cascade Failure algorithm. Results are saved in cf_data
* CF_plot.py: Creates the Betweenness Cascade Failure plots (P(s) ~ nodes_failed)
* requirements.txt: The modules used.

## Why no jupyter notebook?
1. Jupyter notebooks are very bad when used with git. Since they are basically a JSON file, each changed cell or output can lead to a merge conflict. This conflict is non trivial to solve since git only compares the underlining JSON. Over time it wasn't worth the time investment to always solve the merge conflicts.
2. Since betweenness is expensive to compute I decided to parallelise it. Jupyters multiprocessing support is however inadequate. I therefore decided to write my code using classic python files.