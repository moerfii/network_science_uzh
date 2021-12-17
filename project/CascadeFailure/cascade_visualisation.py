from CF_betweenness_parallell import CascadeFailure, BetweennessParallelStrategy
import json





if __name__ == "__main__":
    multiplier="1.5"
    with open(f"cf_data/CF_max_multiplier={multiplier}_BetweennessParallel_k=None_norm=1_weight=travel_time.csv", "r") as f:
        d = f.readlines()
    index = 51
    failed_nodes = json.loads(d[index])["nodes"]
    print(len(failed_nodes))
    bs = BetweennessParallelStrategy(k=None, normalized=True, weight="travel_time")
    cf = CascadeFailure("data/cleaned_manhattan.gml", "data/uncleaned_manhattan.graphml",strategy=bs,multiplier=2.0, init=False)
    cf.failed_nodes = failed_nodes
    cf.create_image(save=True, filepath=f"plots_and_images/cascade_visualisation/visualisation_m={multiplier}[{index}]", show=False)