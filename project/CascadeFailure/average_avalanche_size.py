import matplotlib.pyplot as plt
import json
import numpy as np
import powerlaw
import seaborn as sns
import pandas as pd





def get_data(f):
    data = []
    for i in f:
        data.append(json.loads(i)["nodes"])
    return np.array(data)

def get_average_avalanche(data, ignore_0=False):
    temp = np.zeros((data.shape[0], 100))
    for i in range(data.shape[0]):
        #print(data[i])
        for j in range(len(data[i])):
            print(len(data[i][j]))
            temp[i][j] = len(data[i][j])
    if ignore_0:
        mask = np.where(temp==0)
        temp[mask] = np.nan    
    result = np.nanmean(temp, axis=0)

    return result

def plot(data, label, symbol):
    count = 0
    for i in data:
        if i==0:
            break
        count+=1
    range = np.arange(0,count,1)
    plt.plot(range,data[:count],f"{symbol}", label=f"m={label}")
    

with open("cf_data/CF_max_multiplier=4_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m4 = f.readlines()

with open("f_data/CF_max_multiplier=1.5_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m1_5 = f.readlines()

with open("cf_data/CF_max_multiplier=2.0_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m2 = f.readlines()

with open("cf_data/CF_max_multiplier=3_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
    f_m3 = f.readlines()

data = {
    "1.5" : get_data(f_m1_5),
    "2": get_data(f_m2),
    "3": get_data(f_m3),
    "4": get_data(f_m4)
}

symbols = {
    "1.5": "-",
    "2": "--",
    "3": "-.",
    "4": ":"
}
for key in data.keys():
    mean = get_average_avalanche(data[key])
    plot(mean, key, symbols[key])

plt.title("Average Cascade")
plt.xlabel("t")
plt.ylabel("nodes failed")

plt.legend()
plt.savefig("plots_and_images/average_avalanche.png")
plt.show()

for key in data.keys():
    mean = get_average_avalanche(data[key], ignore_0=True)
    plot(mean, key, symbols[key])

plt.title("Average Cascade, ignore 0")
plt.xlabel("t")
plt.ylabel("nodes failed")

plt.legend()
plt.savefig("plots_and_images/average_avalanche_ignore_0.png")
plt.show()