import subprocess
import random
from multiprocessing import Pool

def run_ranklib(params):
    ntrees, nleaves, shrinkage, mls, tc = params
    cmd = f"java -jar RankLib-2.18.jar -train {train_data} -validate {validation_data} -test {validation_data} -ranker 6 -metric2t NDCG@5 -metric2T NDCG@5 -save model_{ntrees}_{nleaves}_{shrinkage}_{mls}_{tc}.txt -score score_{ntrees}_{nleaves}_{shrinkage}_{mls}_{tc}.txt -tree {ntrees} -leaf {nleaves} -shrinkage {shrinkage} -mls {mls} -tc {tc} -estop 250"
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True)

# Define your parameter ranges
ntrees_range = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1800, 2000, 2100, 2200, 2300, 2400, 2500]
nleaves_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
shrinkage_range = [0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.14, 0.125, 0.11, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
mls_range = [1, 2, 3]
tc_range = [64, 128, 256, 512, 1024, 2048, 3072]

# Define your training and validation data
train_data = "train.txt"
validation_data = "valid.txt"

# Number of iterations for the random search
iterations = 12

# Number of parallel workers (adjust according to your machine's capabilities)
workers = 4

# Generate random parameter combinations
params_list = []
for i in range(iterations):
    params = (
        random.choice(ntrees_range),
        random.choice(nleaves_range),
        random.choice(shrinkage_range),
        random.choice(mls_range),
        random.choice(tc_range),
    )
    params_list.append(params)
    
if __name__ == "__main__":
    # Run RankLib with random parameter combinations in parallel
    with Pool(processes=workers) as pool:
        pool.map(run_ranklib, params_list)