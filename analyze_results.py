#%%
import pandas as pd
from glob import glob
from plotnine import *

#%%
result_files = glob("exp_results/*")
result_files

#%%
result_file = result_files[1]
metadata_splits = result_file.split("/")[1].split(".")[0].split("_")
depth = int(metadata_splits[1].split("-")[1])
parallelism = int(metadata_splits[2].split("-")[1])
iters = int(metadata_splits[3].split("-")[1])

#%%
df = pd.read_csv(result_file, header=None)
df.columns = ["start", "end"]
df["depth"] = depth
df["parallelism"] = parallelism
df["iters"] = iters
df["duration"] = df["end"] - df["start"]
df

#%%
ggplot(df) +\
    geom_boxplot(aes(x="depth", y="duration"))