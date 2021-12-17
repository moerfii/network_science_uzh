import matplotlib.pyplot as plt
import json
import numpy as np
import powerlaw
import seaborn as sns
import pandas as pd




def get_data(f):
    data = []
    for i in f:
        data.append(json.loads(i)["n_failed"])
    return np.array(data)


def plot_hist(data, label, symbol="o"):
    bins=np.array(np.logspace(0, 4,base=10, num=20))
 
    counts,bin_edges = np.histogram(data, bins=bins, density=True )
    bin_centres = bin_edges[:-1]
    plt.scatter(bin_centres, counts, label=f"multiplier={label}", s=20, marker=symbol)

def print_alpha(data):

    fit = powerlaw.Fit(data)

    return fit.alpha

def plot_powerlaw(avalanche):
    
    range = np.linspace(1,4000,4000)
    pl = range**-avalanche
    plt.plot(range, pl, "r--",label=f"powerlaw, avalanche={avalanche}")


with open("cf_data/CF_max_multiplier=4_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m4 = f.readlines()

with open("cf_data/CF_max_multiplier=1.5_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m1_5 = f.readlines()

with open("cf_data/CF_max_multiplier=2.0_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m2 = f.readlines()

with open("cf_data/CF_max_multiplier=3_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m3 = f.readlines()


d_m4 = get_data(f_m4)
d_m1_5 = get_data(f_m1_5)

d_m2 = get_data(f_m2)
d_m3 = get_data(f_m3)



avalanche = 0.1
data = {
    "1.5":d_m1_5,
    "2":d_m2[:100],
    "3": d_m3[:100],
    "4":d_m4[:100]
}

count=0
for key in data.keys():

    alpha = print_alpha(data[key])

    plot_hist(data[key], key)

    plot_powerlaw(alpha)
    plt.legend()
    plt.title(f"Betweenness Cascades, multiplier={key}")
    plt.xlabel("nodes_failed")
    plt.ylabel("P(s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim((0,1e4))
    plt.ylim((1e-5,1e0+0.5))
    plt.savefig(f"plots_and_images/multiplier={key}.png")
    plt.show()
